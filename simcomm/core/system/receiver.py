from typing import List

import numpy as np

from ...utils import pow2db, qfunc
from .system import SystemObject


class Receiver(SystemObject):
    """A class representing a receiver.

    Args:
        sensitivity (float): The sensitivity of the receiver.
        rate (float): The rate of the receiver.
        outage (float): The outage probability of the receiver.

    Attributes:
        name (str): The name of the system object.
        position (List[float]): [x, y] coordinates of the system object.
                                [x, y, z] coordinates if 3D.
    """

    def __init__(self, name: str, position: List[float], sensitivity: float) -> None:
        """
        Initializes a Receiver object with the given parameters.

        Args:
            name: The name of the receiver.
            position: The position of the receiver in 2D or 3D space.
            sensitivity: The sensitivity of the receiver.
        """
        super().__init__(name, position)
        self.sensitivity = sensitivity
        self.rate = None
        self.outage = None

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

    def compute_outage(self, noise_power, sigma):
        """
        Compute the outage probability of the receiver

        Args:
            sigma: Shadowing standard deviation.
        """
        self.outage = qfunc(
            np.mean(
                (pow2db(self.snr) - (-noise_power) - self.sensitivity) / sigma, axis=0
            )
        )
