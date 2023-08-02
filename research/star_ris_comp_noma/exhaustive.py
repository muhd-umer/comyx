"""
Simulates a wireless network with three users and two base stations. The users are U1c,
U2c, and Uf, and the base stations are BS1 and BS2. There is also an RIS element at the
boundary of the transmission radius of both base stations.

BS1 serves U1c and Uf NOMA pair, and BS2 serves U2c and Uf NOMA pair. The RIS element is
used to improve the signal quality of the Uf user. The RIS transmits the signals from the
base stations to the Uf user. It also reflects the impinging signals from the base
stations to the corresponding center users.

Exhaustive search for Element Splitting (ES) and Amplitude Coefficients (Beta) for
RIS-enhanced transmission.
"""

import argparse
import os

import numpy as np
import scipy.io as io
from colorama import Fore, Style
from config import environment, setting

import simcomm.core.propagation as prop
from simcomm.core import STAR, LinkCollection, Receiver, Transmitter
from simcomm.utils import dbm2pow


def main(N, save_path):
    # Load the environment
    pathloss_cfg = environment["pathloss"]
    fading_cfg = environment["fading"]
    positions = environment["positions"]

    # Additional parameters
    BANDWIDTH = 1e6  # Bandwidth in Hz
    TEMP = 300  # Temperature in Kelvin
    FREQ = 2.4e9  # Frequency of carrier signal in Hz

    Pt = -15  # Transmit power in dBm
    Pt_lin = dbm2pow(Pt)  # Transmit power in linear scale
    N0 = prop.get_noise_power(BANDWIDTH, TEMP, 12)  # Noise power in dBm
    N0_lin = dbm2pow(N0)  # Noise power in linear scale

    params = setting["ris70"]
    ris_enhanced = params["ris_enhanced"]  # Whether to use RIS-enhanced transmission
    bs1_uf_link = params["bs1_uf_link"]  # Whether to use BS1-Uf link
    bs2_uf_link = params["bs2_uf_link"]  # Whether to use BS2-Uf link
    K = params["ris_elements"]  # Number of RIS elements

    # Create the base stations
    BS1 = Transmitter("BS1", positions["BS1"], transmit_power=Pt_lin)
    BS2 = Transmitter("BS2", positions["BS2"], transmit_power=Pt_lin)

    # Create the users (identical)
    U1c = Receiver("U1c", positions["U1c"], sensitivity=-110)
    U2c = Receiver("U2c", positions["U2c"], sensitivity=-110)
    Uf = Receiver("Uf", positions["Uf"], sensitivity=-110)

    # Simulate the system
    print(f"{Fore.GREEN}Simulating the system ...{Style.RESET_ALL}")

    beta_r = np.linspace(0, 1, 101)
    beta_t = 1 - beta_r
    bs1_assignment = np.arange(0, K + 1)
    bs2_assignment = K - bs1_assignment
    sum_rate = np.zeros((len(beta_r), len(bs1_assignment)))

    for i in range(len(beta_r)):
        for k in range(len(bs1_assignment)):
            # Create the STAR-RIS element
            RIS = STAR(
                "RIS",
                positions["RIS"],
                elements=K,
                beta_r=beta_r[i],
                beta_t=1 - beta_r[i],
                custom_assignment={"bs1": bs1_assignment[k], "bs2": bs2_assignment[k]},
            )

            # Initialize the link collection (containing channel information)
            links = LinkCollection(N, FREQ)

            # Add the center links to the collection
            links.add_link(
                BS1, U1c, fading_cfg["rayleigh"], pathloss_cfg["center"], "1,c"
            )
            links.add_link(
                BS2, U2c, fading_cfg["rayleigh"], pathloss_cfg["center"], "2,c"
            )

            # Add the edge links to the collection
            links.add_link(
                BS1, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], bs1_uf_link
            )
            links.add_link(
                BS2, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], bs2_uf_link
            )

            # Add the RIS links to the collection
            links.add_link(
                BS1,
                RIS,
                fading_cfg["ricianC"],
                pathloss_cfg["ris"],
                "ris",
                bs1_assignment[k],
            )
            links.add_link(
                BS2,
                RIS,
                fading_cfg["ricianC"],
                pathloss_cfg["ris"],
                "ris",
                bs2_assignment[k],
            )
            links.add_link(
                RIS,
                U1c,
                fading_cfg["ricianC"],
                pathloss_cfg["risOC"],
                "ris",
                bs1_assignment[k],
            )
            links.add_link(
                RIS,
                U2c,
                fading_cfg["ricianC"],
                pathloss_cfg["risOC"],
                "ris",
                bs2_assignment[k],
            )
            links.add_link(
                RIS, Uf, fading_cfg["ricianE"], pathloss_cfg["risOE"], "ris", K
            )

            # Add interference links to the collection
            links.add_link(
                BS1, U2c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "1,c"
            )
            links.add_link(
                BS2, U1c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "2,c"
            )

            # Set the NOMA power allocation
            BS1.set_allocation(U1c, 0.25)
            BS1.set_allocation(Uf, 0.75)
            BS2.set_allocation(U2c, 0.25)
            BS2.set_allocation(Uf, 0.75)

            # Set the RIS phase shifts
            RIS.set_reflection_parameters(links, [BS1, BS2], [U1c, U2c])
            RIS.set_transmission_parameters(links, [BS1, BS2], Uf)

            # Update the link collection
            if ris_enhanced:
                RIS.merge_link(links, BS1, U1c)
                RIS.merge_link(links, BS2, U2c)
                RIS.merge_link(links, [BS1, BS2], Uf)

            # Compute the SNRs
            U1c.snr = BS1.get_allocation(U1c) * (
                (Pt_lin * links.get_gain(BS1, U1c))
                / (Pt_lin * links.get_gain(BS2, U1c) + N0_lin)
            )
            U1c.rate = np.log2(1 + U1c.snr)

            U2c.snr = BS2.get_allocation(U2c) * (
                (Pt_lin * links.get_gain(BS2, U2c))
                / (Pt_lin * links.get_gain(BS1, U2c) + N0_lin)
            )
            U2c.rate = np.log2(1 + U2c.snr)

            snr_BS1 = (Pt_lin * links.get_gain(BS1, Uf)) / N0_lin
            snr_BS2 = (Pt_lin * links.get_gain(BS2, Uf)) / N0_lin
            Uf.snr = (
                BS1.get_allocation(Uf) * snr_BS1 + BS2.get_allocation(Uf) * snr_BS2
            ) / (
                BS1.get_allocation(U1c) * snr_BS1
                + BS2.get_allocation(U2c) * snr_BS2
                + 1
            )
            Uf.rate = np.log2(1 + Uf.snr)

            sum_rate[i, k] = np.mean(U1c.rate + U2c.rate + Uf.rate)

    print(f"{Fore.CYAN}Done!{Style.RESET_ALL}")

    res_file = os.path.join(save_path, f"results_exhaustive_es_aa.mat")

    if save_path is not None:
        io.savemat(
            "results/contour_plot.mat",
            {
                "sum_rate": sum_rate,
                "beta_r": beta_r,
                "beta_t": beta_t,
                "bs1_assignment": bs1_assignment,
                "bs2_assignment": bs2_assignment,
            },
        )
        print(f"{Fore.YELLOW}Results saved to: './{res_file}'{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}Skipping results.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate a wireless network with three users and two base stations."
    )
    parser.add_argument(
        "--realizations",
        type=int,
        default=2000,
        help="Number of channel realizations",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Skip saving results to .mat files",
    )
    args = parser.parse_args()

    if not args.no_save:
        os.makedirs("results", exist_ok=True)
        save_path = "results/"
    else:
        save_path = None

    main(args.realizations, save_path)
