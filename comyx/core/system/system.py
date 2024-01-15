from typing import List


class SystemObject:
    """Base class for all system objects in the network except for the channel.

    Args:
        name: The name of the system object.
        position: The [x, y] or [x, y, z] coordinates of the system object.
    """

    def __init__(self, name: str, position: List[float]):
        """Initializes a SystemObject object with the given parameters."""
        self.name = name
        self.position = position

    def __str__(self):
        """Returns a string representation of the SystemObject."""
        return f"SystemObject(name={self.name}, position={self.position})"
