from typing import List


class SystemObject:
    """Base class for all system objects.

    Attributes:
        name (str): The name of the system object.
        position (List[float]): The [x, y] or [x, y, z] coordinates of the system object.
        antenna_gain (float): The gain of the antenna (G).
        losses (float): The losses of the system object (Lf).
    """

    def __init__(
        self, name: str, position: List[float], antenna_gain: float, losses: float
    ):
        self.name = name
        self.position = position
        self.antenna_gain = antenna_gain
        self.losses = losses

    def __str__(self):
        return f"{self.name} at {self.position}"
