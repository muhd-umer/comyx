from typing import List


class SystemObject:
    """Base class for all system objects.

    Attributes:
        name (str): The name of the system object.
        position (List[float]): The [x, y] or [x, y, z] coordinates of the system object.
    """

    def __init__(self, name: str, position: List[float]):
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.name} at {self.position}"
