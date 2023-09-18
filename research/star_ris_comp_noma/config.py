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
- BS1: [-50, 0, 25]
- BS2: [50, 0, 25]
- RIS: [0, 25, 5]
- Uf: [0, 35, 1]
- U1c: [-40, 18, 1]
- U2c: [30, 22, 1]

Note that the distances can be within +- 5m of the given distance.

Path Loss Exponents (alpha):
- BS1-U1c and BS2-U2c Links = 3
- {BS1, BS2}-Uf Links = 3.5
- {BS1, BS2}-RIS Links = 3
- RIS-{U1c, U2c} Links = 2.7
- RIS-Uf Link = 2.3
- BS2-U1c and BS1-U2c Links = 4

Rician K Factors:
- K1 = 5 dB for RIS-UF Link
- K2 = 3 dB for RIS-{U1C, U2C} Links
"""

environment = {
    "positions": {
        "BS1": [-50, 0, 25],  # BS1 position
        "BS2": [50, 0, 25],  # BS2 position
        "RIS": [0, 25, 5],  # RIS position
        "Uf": [0, 35, 1],  # Uf position
        "U1c": [-40, 18, 1],  # U1c position
        "U2c": [30, 22, 1],  # U2c position
    },
    "fading": {
        "rayleigh": {"type": "rayleigh", "sigma": 1},  # Rayleigh fading
        "ricianE": {
            "type": "rician",
            "K": 4,
            "sigma": 1,
        },  # Rician fading for edge users
        "ricianC": {
            "type": "rician",
            "K": 3,
            "sigma": 1,
        },  # Rician fading for center users
    },
    "pathloss": {
        "center": {"type": "free-space", "alpha": 3, "p0": 30},  # Center users
        "ris": {"type": "free-space", "alpha": 3, "p0": 30},  # BS to RIS
        "risC": {"type": "free-space", "alpha": 2.7, "p0": 30},  # RIS to center users
        "risE": {"type": "free-space", "alpha": 2.3, "p0": 30},  # RIS to edge user
        "edge": {"type": "free-space", "alpha": 3.5, "p0": 30},  # Edge users
        "inter": {"type": "free-space", "alpha": 4, "p0": 30},  # Interference links
    },
}

setting = {
    "ris32": {
        "ris_enhanced": True,  # RIS with 32 elements
        "ris_elements": 32,
        "comp_enabled": True,  # CoMP enabled
    },
    "no_ris": {
        "ris_enhanced": False,  # No RIS
        "comp_enabled": True,  # CoMP enabled"
    },
    "ris70": {
        "ris_enhanced": True,  # RIS with 70 elements
        "ris_elements": 70,
        "comp_enabled": True,  # CoMP enabled
    },
    "no_ris_non_comp": {
        "ris_enhanced": False,  # No RIS
        "comp_enabled": False,  # CoMP disabled
    },
}

constants = {
    "BANDWIDTH": 1e6,  # Bandwidth in Hz
    "TEMP": 300,  # Temperature in Kelvin
    "FREQ": 2.4e9,  # Frequency of carrier signal in Hz
    "SIGMA": 6.32,  # Shadowing standard deviation in dB
}
