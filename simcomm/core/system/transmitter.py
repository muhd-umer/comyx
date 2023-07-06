"""
Implementation of the transmitter class
"""

import numpy as np
import scipy.signal as signal


class Transmitter:
    """
    A class representing a transmitter.

    Attributes:
        tx_power (float): The transmission power of the transmitter.
        tx_antenna_gain (float): The gain of the transmitter antenna.
        tx_frequency (float): The frequency of the transmitter.
    """

    def __init__(self, tx_power, tx_antenna_gain, tx_frequency):
        self.tx_power = tx_power
        self.tx_antenna_gain = tx_antenna_gain
        self.tx_frequency = tx_frequency

    def modulate(self, modulation_type, data, *args, **kwargs):
        """
        Modulate the data with the given modulation type
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
        Perform BPSK modulation on the input data
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
        Perform QPSK modulation on the input data
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
        Perform N-QAM modulation on the input data with the specified value of n
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
