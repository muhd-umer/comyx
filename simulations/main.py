"""
Simulates a wireless network with three users and two base stations. The users are U1C, U2C, and UF, and the base stations are BS1 and BS2. There is also an RIS element at the boundary of the transmission radius of both base stations.

BS1 serves U1C and UF NOMA pair, and BS2 serves U2C and UF NOMA pair. The RIS element is used to improve the signal quality of the UF user. The RIS transmits the signals from the base stations to the UF user. It also reflects the impinging signals from the base stations to the corresponding center users.
"""

import os
import sys

# Append the path depending on where the script is executed
if os.path.basename(os.getcwd()) == "simulations":
    sys.path.append("..")
elif os.path.basename(os.getcwd()) == "comm-fyp":
    sys.path.append(".")
else:
    raise Exception(
        "Please execute this script from eiher simcomm/ or simulations/ folder."
    )

import numpy as np
from colorama import Fore, Style
from config import configs

import simcomm.core.propagation as prop
from simcomm.core import STAR, LinkCollection, Receiver, Transmitter
from simcomm.utils import dbm2pow, pow2db, qfunc

# Load the environment
environment = configs
pathloss_cfg = environment["pathloss"]
fading_cfg = environment["fading"]
positions = environment["positions"]

# Additional parameters
BANDWIDTH = 1e6  # Bandwidth in Hz
TEMP = 300  # Temperature in Kelvin
FREQ = 27e9  # Frequency of carrier signal in Hz
SIGMA = 8  # Shadowing standard deviation in dB

Pt = np.linspace(-50, 30, 80)  # Transmit power in dBm
Pt_lin = dbm2pow(Pt)  # Transmit power in linear scale
N0 = prop.get_noise_power(BANDWIDTH, TEMP, 12)  # Noise power in dBm
N0_lin = dbm2pow(N0)  # Noise power in linear scale

N_sim = 2000  # Number of simulations
M = 12  # Number of RIS elements

# Create the base stations
BS1 = Transmitter("BS1", positions["BS1"], transmit_power=Pt_lin)
BS2 = Transmitter("BS2", positions["BS2"], transmit_power=Pt_lin)

# Create the users (identical)
U1C = Receiver("U1C", positions["U1C"], margin=8, sensitivity=-110)
U2C = Receiver("U2C", positions["U2C"], margin=8, sensitivity=-110)
UF = Receiver("UF", positions["UF"], margin=8, sensitivity=-110)

# Create the STAR-RIS element
RIS = STAR("RIS", positions["RIS"], elements=M)

# Initialize the link collection (containing channel information)
links = LinkCollection(N_sim, FREQ)

# Add the center links to the collection
links.add_link(BS1, U1C, fading_cfg["rayleigh"], pathloss_cfg["center"], "1C")
links.add_link(BS2, U2C, fading_cfg["rayleigh"], pathloss_cfg["center"], "2C")

# Add the edge links to the collection
links.add_link(BS1, UF, fading_cfg["rayleigh"], pathloss_cfg["edge"], "DNE")
links.add_link(BS2, UF, fading_cfg["rayleigh"], pathloss_cfg["edge"], "DNE")

# Add the RIS links to the collection
links.add_link(BS1, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "RIS", M // 2)
links.add_link(BS2, RIS, fading_cfg["ricianC"], pathloss_cfg["ris"], "RIS", M // 2)
links.add_link(RIS, U1C, fading_cfg["ricianC"], pathloss_cfg["risOC"], "RIS", M // 2)
links.add_link(RIS, U2C, fading_cfg["ricianC"], pathloss_cfg["risOC"], "RIS", M // 2)
links.add_link(RIS, UF, fading_cfg["ricianE"], pathloss_cfg["risOE"], "RIS", M)

# Add interference links to the collection
links.add_link(BS1, U2C, fading_cfg["rayleigh"], pathloss_cfg["inter"], "1C")
links.add_link(BS2, U1C, fading_cfg["rayleigh"], pathloss_cfg["inter"], "2C")

# Simulate the system
print(f"{Fore.GREEN}Simulating the system ...{Style.RESET_ALL}")

# Set the NOMA power allocation
BS1.set_allocation(U1C, 0.2)
BS1.set_allocation(UF, 0.8)
BS2.set_allocation(U2C, 0.2)
BS2.set_allocation(UF, 0.8)

# Set the RIS phase shifts
RIS.set_reflection_parameters(links, [BS1, BS2], [U1C, U2C])
RIS.set_transmission_parameters(links, [BS1, BS2], UF)

# Update the link collection
RIS.merge_link(links, BS1, U1C)
RIS.merge_link(links, BS2, U2C)
RIS.merge_link(links, [BS1, BS2], UF)

sum_rate = np.zeros((N_sim, len(Pt)))

# Compute the SNRs
U1C.snr = BS2.get_allocation(U2C) * (
    (Pt_lin * links.get_gain(BS1, U1C)) / (Pt_lin * links.get_gain(BS2, U1C) + N0_lin)
)
U1C.rate = np.log2(1 + U1C.snr)

U2C.snr = BS2.get_allocation(U2C) * (
    (Pt_lin * links.get_gain(BS2, U2C)) / (Pt_lin * links.get_gain(BS1, U2C) + N0_lin)
)
U2C.rate = np.log2(1 + U2C.snr)

UF.snr_BS1 = (Pt_lin * links.get_gain(BS1, UF)) / N0_lin
UF.snr_BS2 = (Pt_lin * links.get_gain(BS2, UF)) / N0_lin
UF.snr = (BS1.get_allocation(UF) * UF.snr_BS1 + BS2.get_allocation(UF) * UF.snr_BS2) / (
    BS1.get_allocation(U1C) * UF.snr_BS1 + BS2.get_allocation(U2C) * UF.snr_BS2 + 1
)
UF.rate = np.log2(1 + UF.snr)

sum_rate = np.mean(U1C.rate + U2C.rate + UF.rate, axis=0)

U1C.outage = qfunc(np.mean((pow2db(U1C.snr) - (-N0) - U1C.sensitivity) / 7.2, axis=0))
U2C.outage = qfunc(np.mean((pow2db(U2C.snr) - (-N0) - U2C.sensitivity) / 7.2, axis=0))
UF.outage = qfunc(np.mean((pow2db(UF.snr) - (-N0) - UF.sensitivity) / 7.2, axis=0))

print(f"{Fore.CYAN}Done!{Style.RESET_ALL}")
