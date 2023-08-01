from typing import List


class SystemObject:
    """Base class for all system objects.

    Attributes:
        name (str): The name of the system object.
        position (array_like): The [x, y] or [x, y, z] coordinates of the system object.
    """

    def __init__(self, name: str, position: List[float]):
        """Initializes a SystemObject object with the given parameters.

        Args:
            name (str): The name of the system object.
            position (list): The [x, y] or [x, y, z] coordinates of the system object.
        """
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.name} at {self.position}"


__all__ = ["SystemObject"]
