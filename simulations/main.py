"""
Simulates a wireless network with three users and two base stations. The users are U1C, U2C, and UF, and the base stations are BS1 and BS2. There is also an RIS element at the boundary of the transmission radius of both base stations.

BS1 serves U1C and UF NOMA pair, and BS2 serves U2C and UF NOMA pair. The RIS element is used to improve the signal quality of the UF user. The RIS transmits the signals from the base stations to the UF user. It also reflects the impinging signals from the base stations to the corresponding center users.

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
- RIS-UF Link = 2.3
- BS2-U1C and BS1-U2C Links = 4

Rician K Factors:
- K1 = 5 dB for RIS-UF Link
- K2 = 3 dB for RIS-{U1C, U2C} Links

Shadowing (sigma):
- NLOS Links = 7.8 dB
- LOS Links = 3.5 dB

The rest of the parameters are variable in nature, and are defined when creating system objects.
"""
