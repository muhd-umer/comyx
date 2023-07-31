"""
Simulates a wireless network with three users and two base stations. The users are U1c,
U2c, and Uf, and the base stations are BS1 and BS2. There is also an RIS element at the
boundary of the transmission radius of both base stations.

BS1 serves U1c and Uf NOMA pair, and BS2 serves U2c and Uf NOMA pair. The RIS element is
used to improve the signal quality of the Uf user. The RIS transmits the signals from the
base stations to the Uf user. It also reflects the impinging signals from the base
stations to the corresponding center users.
"""

import argparse
import os
import sys

# Append the path depending on where the script is executed
if os.path.basename(os.getcwd()) == "simulations":
    sys.path.append("..")
    os.makedirs("results", exist_ok=True)
    save_path = "results/"
elif os.path.basename(os.getcwd()) == "comm-fyp":
    sys.path.append(".")
    os.makedirs("simulations/results", exist_ok=True)
    save_path = "simulations/results/"
else:
    raise Exception(
        "Please execute this script from either simcomm/ or simulations/ folder."
    )

import numpy as np
import scipy.io as io
from colorama import Fore, Style
from config import environment, setting

import simcomm.core.propagation as prop
from simcomm.core import STAR, LinkCollection, Receiver, Transmitter
from simcomm.utils import dbm2pow, pow2db, qfunc


def main(N, link_option, custom_run, save_path):
    # Load the environment
    pathloss_cfg = environment["pathloss"]
    fading_cfg = environment["fading"]
    positions = environment["positions"]

    # Additional parameters
    BANDWIDTH = 1e6  # Bandwidth in Hz
    TEMP = 300  # Temperature in Kelvin
    FREQ = 2.4e9  # Frequency of carrier signal in Hz
    SIGMA = 6.32  # Shadowing standard deviation in dB

    Pt = np.linspace(-50, 30, 161)  # Transmit power in dBm
    Pt_lin = dbm2pow(Pt)  # Transmit power in linear scale
    N0 = prop.get_noise_power(BANDWIDTH, TEMP, 12)  # Noise power in dBm
    N0_lin = dbm2pow(N0)  # Noise power in linear scale
    P_circuit = 10 ** (-3)  # Circuit power in watts

    params = setting[link_option]
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

    bs1_assignment = K // 2
    bs2_assignment = K - bs1_assignment

    # Create the STAR-RIS element
    RIS = STAR("RIS", positions["RIS"], elements=K)

    # Initialize the link collection (containing channel information)
    links = LinkCollection(N, FREQ)

    # Add the center links to the collection
    links.add_link(BS1, U1c, fading_cfg["rayleigh"], pathloss_cfg["center"], "1,c")
    links.add_link(BS2, U2c, fading_cfg["rayleigh"], pathloss_cfg["center"], "2,c")

    # Add the edge links to the collection
    links.add_link(BS1, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], bs1_uf_link)
    links.add_link(BS2, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], bs2_uf_link)

    # Add the RIS links to the collection
    links.add_link(
        BS1, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris", bs1_assignment
    )
    links.add_link(
        BS2, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris", bs2_assignment
    )
    links.add_link(
        RIS, U1c, fading_cfg["ricianC"], pathloss_cfg["risOC"], "ris", bs1_assignment
    )
    links.add_link(
        RIS, U2c, fading_cfg["ricianC"], pathloss_cfg["risOC"], "ris", bs2_assignment
    )
    links.add_link(RIS, Uf, fading_cfg["ricianE"], pathloss_cfg["risOE"], "ris", K)

    # Add interference links to the collection
    links.add_link(BS1, U2c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "1,c")
    links.add_link(BS2, U1c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "2,c")
    # Simulate the system
    print(f"{Fore.GREEN}Simulating the system ...{Style.RESET_ALL}")

    # Set the NOMA power allocation
    BS1.set_allocation(U1c, 0.3)
    BS1.set_allocation(Uf, 0.7)
    BS2.set_allocation(U2c, 0.3)
    BS2.set_allocation(Uf, 0.7)

    # Set the RIS phase shifts
    RIS.set_reflection_parameters(links, [BS1, BS2], [U1c, U2c])
    RIS.set_transmission_parameters(links, [BS1, BS2], Uf)

    # Update the link collection
    if ris_enhanced:
        RIS.merge_link(links, BS1, U1c)
        RIS.merge_link(links, BS2, U2c)
        RIS.merge_link(links, [BS1, BS2], Uf)

    sum_rate = np.zeros((N, len(Pt)))

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

    ## NonCoMP
    # snr_BS1 = (Pt_lin * links.get_gain(BS1, Uf)) / (
    #     N0_lin + Pt_lin * links.get_gain(BS2, Uf)
    # )
    # snr_BS2 = (Pt_lin * links.get_gain(BS2, Uf)) / (
    #     N0_lin + Pt_lin * links.get_gain(BS1, Uf)
    # )

    # CoMP
    snr_BS1 = (Pt_lin * links.get_gain(BS1, Uf)) / N0_lin
    snr_BS2 = (Pt_lin * links.get_gain(BS2, Uf)) / N0_lin

    Uf.snr = (BS1.get_allocation(Uf) * snr_BS1 + BS2.get_allocation(Uf) * snr_BS2) / (
        BS1.get_allocation(U1c) * snr_BS1 + BS2.get_allocation(U2c) * snr_BS2 + 1
    )
    Uf.rate = np.log2(1 + Uf.snr)

    sum_rate = np.mean(U1c.rate + U2c.rate + Uf.rate, axis=0)
    energy_efficiency = sum_rate / (Pt_lin * 2 + P_circuit)
    spectral_efficiency = sum_rate

    U1c.outage = np.mean(
        qfunc((pow2db(U1c.snr) - (-N0) - U1c.sensitivity) / SIGMA), axis=0
    )
    U2c.outage = np.mean(
        qfunc((pow2db(U2c.snr) - (-N0) - U2c.sensitivity) / SIGMA), axis=0
    )
    Uf.outage = np.mean(
        qfunc((pow2db(Uf.snr) - (-N0) - Uf.sensitivity) / SIGMA), axis=0
    )

    print(f"{Fore.CYAN}Done!{Style.RESET_ALL}")

    if not custom_run:
        res_file = os.path.join(save_path, f"results_{link_option}.mat")
    else:
        res_file = os.path.join(save_path, f"results_{link_option}_custom.mat")

    tx_power = os.path.join(save_path, f"tx_power_dB.mat")

    # Save the results
    io.savemat(
        res_file,
        {
            "rates": [
                np.mean(U1c.rate, axis=0),
                np.mean(U2c.rate, axis=0),
                np.mean(Uf.rate, axis=0),
            ],
            "sum_rate": sum_rate,
            "outage": [U1c.outage, U2c.outage, Uf.outage],
            "se": spectral_efficiency,
            "ee": energy_efficiency,
        },
    )
    io.savemat(tx_power, {"tx_power": Pt})

    print(f"{Fore.YELLOW}Results saved to: './{res_file}'{Style.RESET_ALL}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate a wireless network with three users and two base stations."
    )
    parser.add_argument(
        "--realizations",
        type=int,
        default=5000,
        help="Number of channel realizations",
    )
    parser.add_argument(
        "--setting",
        type=str,
        default="ris32",
        choices=setting.keys(),
        help="Link option",
    )
    parser.add_argument(
        "--custom",
        action="store_true",
        help="Whether to use custom power allocation",
    )
    args = parser.parse_args()
    main(args.realizations, args.setting, args.custom, save_path)
