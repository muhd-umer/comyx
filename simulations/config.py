"""
Positions (x, y, z):
- BS1 is the center user for U1C, and BS2 is the center user for U2C
- Both base stations are at z = 25, and the RIS is at z = 10
- The distances between the elements are around:
    - BS1 to U1C and BS2 to U2C distance ≈ 25m
    - BS1 to UF and BS2 to UF distance ≈ 65m
    - BS1 to RIS and BS2 to RIS distance ≈ 55m
    - RIS to UF distance ≈ 15m
    - RIS to U1C and RIS to U2C distance ≈ 40m
    - BS2 to U1C and BS1 to U2C distance ≈ 90m

The 3D position components for each element of the system are generated as follows:
- BS1 = np.array([-50, 0, 25])
- BS2 = np.array([50, 0, 25])
- RIS = np.array([0, 25, 10])
- UF = np.array([0, 40, 1])
- U1C = np.array([-40, 20, 1])
- U2C = np.array([40, 20, 1])

Note that the distances can be within +- 5m of the given distance.

Path Loss Exponents (alpha):
- BS1-U1C and BS2-U2C Links = 3
- {BS1, BS2}-UF Links = 3.5
- {BS1, BS2}-RIS Links = 3
- RIS-{U1C, U2C} Links = 2.7
- RIS-UF Link = 2.4
- BS2-U1C and BS1-U2C Links = 4

Rician K Factors:
- K1 = 5 dB for RIS-UF Link
- K2 = 3 dB for RIS-{U1C, U2C} Links

Shadowing (sigma):
- NLOS Links = 7.8 dB
- LOS Links = 3.5 dB

The rest of the parameters are variable in nature, and are defined when creating system objects.
"""

environment = {
    "positions": {
        "BS1": [-50, 0, 25],
        "BS2": [50, 0, 25],
        "RIS": [0, 25, 5],
        "Uf": [0, 35, 1],
        "U1c": [-40, 18, 1],
        "U2c": [30, 22, 1],
    },
    "fading": {
        "rayleigh": {"type": "rayleigh", "sigma": 1},
        "ricianE": {"type": "rician", "K": 4, "sigma": 1},
        "ricianC": {"type": "rician", "K": 2, "sigma": 1},
    },
    "pathloss": {
        "center": {"type": "free-space", "alpha": 3, "p0": 30},
        "ris": {"type": "free-space", "alpha": 3, "p0": 30},
        "risOC": {"type": "free-space", "alpha": 2.7, "p0": 30},
        "risOE": {"type": "free-space", "alpha": 2.3, "p0": 30},
        "edge": {"type": "free-space", "alpha": 3.5, "p0": 30},
        "inter": {"type": "free-space", "alpha": 4, "p0": 30},
    },
}

setting = {
    "both": {
        "ris_enhanced": True,
        "bs1_uf_link": "E",
        "bs2_uf_link": "E",
    },
    "bs1_only": {
        "ris_enhanced": True,
        "bs1_uf_link": "E",
        "bs2_uf_link": "DNE",
    },
    "bs2_only": {
        "ris_enhanced": True,
        "bs1_uf_link": "DNE",
        "bs2_uf_link": "E",
    },
    "none": {
        "ris_enhanced": True,
        "bs1_uf_link": "DNE",
        "bs2_uf_link": "DNE",
    },
    "no_ris": {
        "ris_enhanced": False,
        "bs1_uf_link": "E",
        "bs2_uf_link": "E",
    },
}
