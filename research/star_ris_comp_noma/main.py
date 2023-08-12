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

import numpy as np
from config import constants, environment, setting

import simcomm.core.propagation as prop
from simcomm.core import STAR, LinkCollection, Receiver, Simulator, Transmitter
from simcomm.utils import dbm2pow


def main(N, link_option, custom_run, save_path):
    # Load the environment
    pathloss_cfg = environment["pathloss"]
    fading_cfg = environment["fading"]
    positions = environment["positions"]

    # Additional parameters
    BANDWIDTH = constants["BANDWIDTH"]  # Bandwidth in Hz
    TEMP = constants["TEMP"]  # Temperature in Kelvin
    FREQ = constants["FREQ"]  # Frequency of carrier signal in Hz
    SIGMA = constants["SIGMA"]  # Shadowing standard deviation in dB

    Pt = np.linspace(-50, 30, 161)  # Transmit power in dBm
    Pt_lin = dbm2pow(Pt)  # Transmit power in linear scale
    N0 = prop.get_noise_power(BANDWIDTH, TEMP, 12)  # Noise power in dBm
    P_circuit = 10 ** (-3)  # Circuit power in watts

    params = setting[link_option]
    ris_enhanced = params["ris_enhanced"]  # Whether to use RIS-enhanced transmission
    comp_enabled = params["comp_enabled"]  # Whether to use computation offloading

    # Create the base stations
    BS1 = Transmitter("BS1", positions["BS1"], Pt_lin, {"U1c": 0.3, "Uf": 0.7})
    BS2 = Transmitter("BS2", positions["BS2"], Pt_lin, {"U2c": 0.3, "Uf": 0.7})

    # Create the users (identical)
    U1c = Receiver("U1c", positions["U1c"], sensitivity=-110)
    U2c = Receiver("U2c", positions["U2c"], sensitivity=-110)
    Uf = Receiver("Uf", positions["Uf"], sensitivity=-110)

    # Initialize the link collection (containing channel information)
    links = LinkCollection(N, FREQ)

    # Add the center links to the collection
    links.add_link(BS1, U1c, fading_cfg["rayleigh"], pathloss_cfg["center"], "1,c")
    links.add_link(BS2, U2c, fading_cfg["rayleigh"], pathloss_cfg["center"], "2,c")

    # Add the edge links to the collection
    links.add_link(BS1, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], "f")
    links.add_link(BS2, Uf, fading_cfg["rayleigh"], pathloss_cfg["edge"], "f")

    # Add interference links to the collection
    links.add_link(BS1, U2c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "i,c")
    links.add_link(BS2, U1c, fading_cfg["rayleigh"], pathloss_cfg["inter"], "i,c")

    # Update the link collection
    if ris_enhanced:
        K = params["ris_elements"]  # Number of RIS elements

        # Create the STAR-RIS element
        RIS = STAR("RIS", positions["RIS"], elements=K)

        # Add the RIS links to the collection
        links.add_link(BS1, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris,b1")
        links.add_link(BS2, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "ris,b2")
        links.add_link(RIS, U1c, fading_cfg["ricianC"], pathloss_cfg["risC"], "ris,b1")
        links.add_link(RIS, U2c, fading_cfg["ricianC"], pathloss_cfg["risC"], "ris,b2")
        links.add_link(RIS, Uf, fading_cfg["ricianE"], pathloss_cfg["risE"], "ris,f")
    else:
        RIS = None

    # Simulate the system
    simulator = Simulator(
        [BS1, BS2], [U1c, U2c, Uf], link_option, RIS, custom_run, save_path
    )
    simulator.run(N, Pt, N0, links, SIGMA, P_circuit, comp=comp_enabled)


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
        save_path = ""

    main(args.realizations, args.setting, args.custom, save_path)
