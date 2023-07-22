import numpy as np

from .system import SystemObject


class Transmitter(SystemObject):
    """A class representing a transmitter.

    This class inherits from SystemObject and represents a transmitter object in a wireless communication system.

    Attributes:
        name (str): The name of the transmitter.
        position (list): The position of the transmitter in 2D or 3D space.
        antenna_gain (float): The gain of the transmitter's antenna.
        losses (float): The losses of the transmitter.
        transmit_power (float): The transmit power of the transmitter.
        allocations (dict): A dictionary of power allocations for the receivers.

    Inherited Attributes:
        name (str): The name of the system object.
        position (list): The position of the system object in 2D or 3D space.
    """

    def __init__(self, name, position, transmit_power):
        """Initializes a Transmitter object with the given parameters.

        Args:
            name: The name of the transmitter.
            position: The position of the transmitter in 2D or 3D space.
            transmit_power: The transmit power of the transmitter.

        Attributes:
            name (str): The name of the transmitter.
            position (list): The position of the transmitter in 2D or 3D space.
            transmit_power (float): The transmit power of the transmitter.
            allocations (dict): A dictionary of power allocations for the receivers.
        """
        super().__init__(name, position)
        self.transmit_power = transmit_power
        self.allocations = {}

    def set_allocation(self, receiver, allocation):
        """
        Sets the power allocation for a given receiver.
        """
        self.allocations[receiver.name] = allocation

    def get_allocation(self, receiver):
        """
        Gets the power allocation for a given receiver.
        """
        return self.allocations[receiver.name]

    def modulate(self, modulation_type, data, *args, **kwargs):
        """
        Modulates the input data with the given modulation type.
        """
        if modulation_type == "bpsk":
            return self.bpsk_modulation(data)
        elif modulation_type == "qpsk":
            return self.qpsk_modulation(data)
        elif modulation_type == "nqam":
            n = kwargs.get("n", 16)  # Default value for n is 16 if not provided
            return self.nqam_modulation(data, n)
        else:
            raise ValueError(
                "Modulation type {} is not supported".format(modulation_type)
            )

    def bpsk_modulation(self, data):
        """
        Performs BPSK modulation on the input data.
        """
        modulated_data = np.zeros(len(data), dtype=np.complex64)
        for i, bit in enumerate(data):
            if bit == 0:
                modulated_data[i] = -1.0 + 0j
            else:
                modulated_data[i] = 1.0 + 0j
        return modulated_data

    def qpsk_modulation(self, data):
        """
        Performs QPSK modulation on the input data.
        """
        modulated_data = np.zeros(len(data) // 2, dtype=np.complex64)
        for i in range(len(data) // 2):
            index = i * 2
            bit1, bit2 = data[index], data[index + 1]
            if bit1 == 0 and bit2 == 0:
                modulated_data[i] = (-1.0 + 1j) / np.sqrt(2)
            elif bit1 == 0 and bit2 == 1:
                modulated_data[i] = (-1.0 - 1j) / np.sqrt(2)
            elif bit1 == 1 and bit2 == 0:
                modulated_data[i] = (1.0 + 1j) / np.sqrt(2)
            else:
                modulated_data[i] = (1.0 - 1j) / np.sqrt(2)
        return modulated_data

    def nqam_modulation(self, data, n):
        """
        Performs N-QAM modulation on the input data with the specified value of n.
        """
        if n < 4 or n % 2 != 0:
            raise ValueError("Invalid value of n for N-QAM modulation")

        m = int(np.log2(n))  # Number of bits per symbol

        modulated_data = np.zeros(len(data) // m, dtype=np.complex64)
        for i in range(len(data) // m):
            index = i * m
            symbol_bits = data[index : index + m]

            symbol = 0
            for j, bit in enumerate(symbol_bits):
                symbol += bit * 2 ** (m - 1 - j)

            if symbol < n // 2:
                modulated_data[i] = (2 * symbol - n + 1) / np.sqrt(n)
            else:
                modulated_data[i] = (2 * (symbol - n // 2) - n + 2) / np.sqrt(n)
        return modulated_data
        return modulated_data
