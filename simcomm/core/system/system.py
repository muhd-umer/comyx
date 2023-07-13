"""
Implement the System class, Base class for all system objects.
"""

import numpy as np


class SystemObject:
    """
    Base class for all system objects.

    Attributes:
        name: The name of the system object.
        position: [x, y] coordinates of the system object.
                  [x, y, z] coordinates if 3D.
        antenna_gain: G, the gain of the antenna.
        losses: Lf, the losses of the system object.
    """

    def __init__(self, name, position, antenna_gain, losses):
        self.name = name
        self.position = position
        self.antenna_gain = antenna_gain
        self.losses = losses

    def __str__(self):
        return f"{self.name} at {self.position}"
