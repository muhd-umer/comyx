"""
Implementation of the reciever class.
"""

import numpy as np


class Reciever:
    """
    A class representing a receiver.

    Attributes:
        rx_antenna_gain (float): The gain of the receiver antenna.
        rx_sensitivity (float): The sensitivity of the receiver in dBm.
    """

    def __init__(self, rx_antenna_gain, rx_frequency):
        self.rx_antenna_gain = rx_antenna_gain
        self.rx_frequency = rx_frequency

    def demodulate(self, modulation_type, received_signal, *args, **kwargs):
        """
        Demodulate the received signal using the specified modulation type
        """
        if modulation_type == "bpsk":
            return self.bpsk_demodulation(received_signal)
        elif modulation_type == "qpsk":
            return self.qpsk_demodulation(received_signal)
        elif modulation_type == "nqam":
            n = kwargs.get("n", 16)  # Default value for n is 16 if not provided
            return self.nqam_demodulation(received_signal, n)
        else:
            raise ValueError(
                "Modulation type {} is not supported".format(modulation_type)
            )

    def bpsk_demodulation(self, received_signal):
        """
        Perform BPSK demodulation on the received signal
        """
        demodulated_data = np.zeros(len(received_signal), dtype=int)
        for i, sample in enumerate(received_signal):
            if sample.real < 0:
                demodulated_data[i] = 0
            else:
                demodulated_data[i] = 1
        return demodulated_data

    def qpsk_demodulation(self, received_signal):
        """
        Perform QPSK demodulation on the received signal
        """
        demodulated_data = np.zeros(2 * len(received_signal), dtype=int)
        for i, sample in enumerate(received_signal):
            if sample.real < 0:
                demodulated_data[2 * i] = 0
            else:
                demodulated_data[2 * i] = 1

            if sample.imag < 0:
                demodulated_data[2 * i + 1] = 0
            else:
                demodulated_data[2 * i + 1] = 1
        return demodulated_data

    def nqam_demodulation(self, received_signal, n):
        """
        Perform N-QAM demodulation on the received signal with the specified value of n
        """
        if n < 4 or n % 2 != 0:
            raise ValueError("Invalid value of n for N-QAM modulation")

        m = int(np.log2(n))  # Number of bits per symbol

        demodulated_data = np.zeros(m * len(received_signal), dtype=int)
        for i, sample in enumerate(received_signal):
            if sample.real < 0:
                symbol_re = 0
            else:
                symbol_re = 1

            if sample.imag < 0:
                symbol_im = 0
            else:
                symbol_im = 1

            symbol = symbol_re * 2 + symbol_im

            symbol_bits = np.zeros(m, dtype=int)
            for j in range(m):
                symbol_bits[m - 1 - j] = symbol % 2
                symbol //= 2

            demodulated_data[i * m : (i + 1) * m] = symbol_bits

        return demodulated_data
