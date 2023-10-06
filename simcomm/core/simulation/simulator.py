from __future__ import annotations

import os
from typing import Any, List, Union

import numpy as np
import numpy.typing as npt
import scipy.io as io
from colorama import Fore, Style

from ...utils import dbm2pow, pow2db, qfunc
from ..system import STAR, LinkCollection, Receiver, Transmitter

NDArrayFloat = npt.NDArray[np.floating[Any]]


class Simulator:
    """Simulator for the wireless communication system consisting of transmitters,
    receivers, and STAR-RIS links.

    Args:
        transmitters: List of transmitters (BSs) in the system.
        receivers: List of receivers (users) in the system.
        link_option: Link option for the simulation.
        star: STAR-RIS array.
        custom_run: Whether to run a custom simulation or not.
        save_path: Path to save the results.

    Attributes:
        BS1: First transmitter (BS).
        BS2: Second transmitter (BS).
        U1c: First receiver (near user closer to BS1).
        U2c: Second receiver (near user closer to BS2).
        Uf: Third receiver (far user).
        star: STAR-RIS array.
        energy_efficiency: Energy efficiency of the system.
        spectral_efficiency: Spectral efficiency of the system.
    """

    def __init__(
        self,
        transmitters: List[Transmitter],
        receivers: List[Receiver],
        link_option: str,
        star: Union[STAR, None] = None,
        custom_run: bool = False,
        save_path: str = "",
    ) -> None:
        self.BS1, self.BS2 = transmitters
        self.U1c, self.U2c, self.Uf = receivers
        self.star = star
        self.energy_efficiency = None
        self.spectral_efficiency = None
        self.link_option = link_option
        self.custom_run = custom_run
        self.save_path = save_path

    def run(
        self,
        N: int,
        Pt: NDArrayFloat,
        N0: NDArrayFloat,
        links: LinkCollection,
        sigma: float,
        P_circuit: float,
        comp: bool = True,
    ) -> None:
        """Run the simulation for the given number of realizations.

        Args:
            N: Number of realizations.
            Pt: Transmitter power in dBm.
            N0: Noise power in dBm.
            links: Link collection.
            sigma: Shadowing standard deviation in dB.
            P_circuit: Circuit power in Watts.
            comp: Whether to use CoMP or not.
        """
        print(f"{Fore.GREEN}Running the simulation...{Style.RESET_ALL}")

        if self.star is not None:
            # Set the RIS phase shifts
            self.star.set_reflection_parameters(
                links, [self.BS1, self.BS2], [self.U1c, self.U2c]
            )
            self.star.set_transmission_parameters(links, [self.BS1, self.BS2], self.Uf)

            # Merge the links
            self.star.merge_link(links, self.BS1, self.U1c)
            self.star.merge_link(links, self.BS2, self.U2c)
            self.star.merge_link(links, [self.BS1, self.BS2], self.Uf)

        Pt_lin = dbm2pow(Pt)
        N0_lin = dbm2pow(N0)

        sum_rate = np.zeros((N, len(Pt)))

        # Compute the SNRs
        self.U1c.snr = self.BS1.get_allocation(self.U1c) * (
            (Pt_lin * links.get_gain(self.BS1, self.U1c))
            / (Pt_lin * links.get_gain(self.BS2, self.U1c) + N0_lin)
        )
        self.U1c.rate = np.log2(1 + self.U1c.snr)

        self.U2c.snr = self.BS2.get_allocation(self.U2c) * (
            (Pt_lin * links.get_gain(self.BS2, self.U2c))
            / (Pt_lin * links.get_gain(self.BS1, self.U2c) + N0_lin)
        )
        self.U2c.rate = np.log2(1 + self.U2c.snr)

        if not comp:
            snr_BS1 = (Pt_lin * links.get_gain(self.BS1, self.Uf)) / (
                N0_lin + Pt_lin * links.get_gain(self.BS2, self.Uf)
            )
            snr_BS2 = (Pt_lin * links.get_gain(self.BS2, self.Uf)) / (
                N0_lin + Pt_lin * links.get_gain(self.BS1, self.Uf)
            )

        else:
            snr_BS1 = (Pt_lin * links.get_gain(self.BS1, self.Uf)) / N0_lin
            snr_BS2 = (Pt_lin * links.get_gain(self.BS2, self.Uf)) / N0_lin

        self.Uf.snr = (
            self.BS1.get_allocation(self.Uf) * snr_BS1
            + self.BS2.get_allocation(self.Uf) * snr_BS2
        ) / (
            self.BS1.get_allocation(self.U1c) * snr_BS1
            + self.BS2.get_allocation(self.U2c) * snr_BS2
            + 1
        )
        self.Uf.rate = np.log2(1 + self.Uf.snr)

        sum_rate = np.mean(self.U1c.rate + self.U2c.rate + self.Uf.rate, axis=0)
        self.energy_efficiency = sum_rate / (Pt_lin * 2 + P_circuit)
        self.spectral_efficiency = sum_rate

        self.U1c.outage = np.mean(
            qfunc((pow2db(self.U1c.snr) - (-N0) - self.U1c.sensitivity) / sigma), axis=0
        )
        self.U2c.outage = np.mean(
            qfunc((pow2db(self.U2c.snr) - (-N0) - self.U2c.sensitivity) / sigma), axis=0
        )
        self.Uf.outage = np.mean(
            qfunc((pow2db(self.Uf.snr) - (-N0) - self.Uf.sensitivity) / sigma), axis=0
        )

        print(f"{Fore.CYAN}Done!{Style.RESET_ALL}")

        if self.save_path != "":
            if not self.custom_run:
                res_file = os.path.join(
                    self.save_path, f"results_{self.link_option}.mat"
                )
            else:
                res_file = os.path.join(
                    self.save_path, f"results_{self.link_option}_custom.mat"
                )

            tx_power = os.path.join(self.save_path, f"tx_power_dB.mat")

            # Save the results
            io.savemat(
                res_file,
                {
                    "rates": [
                        np.mean(self.U1c.rate, axis=0),
                        np.mean(self.U2c.rate, axis=0),
                        np.mean(self.Uf.rate, axis=0),
                    ],
                    "sum_rate": sum_rate,
                    "outage": [self.U1c.outage, self.U2c.outage, self.Uf.outage],
                    "se": self.spectral_efficiency,
                    "ee": self.energy_efficiency,
                },
            )
            io.savemat(tx_power, {"tx_power": Pt})

            print(f"\n{Fore.YELLOW}Results saved to: './{res_file}'{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}Skipping results.\n")
