from scipy.constants import Boltzmann

from simcomm.utils import pow2db, pow2dbm


def thermal_noise(bandwidth: float, temperature: float = 300) -> float:
    """Compute the thermal noise.

    Args:
        bandwidth: Bandwidth in Hz.
        temperature: Temperature in Kelvin.

    Returns:
        Thermal noise.
    """
    return Boltzmann * temperature


def get_noise_power(
    noise_figure: float, bandwidth: float, temperature: float = 300
) -> float:
    """Compute the noise power in dBm.

    Args:
        noise_figure: Noise figure in dB.
        bandwidth: Bandwidth in Hz.
        temperature: Temperature in Kelvin.

    Returns:
        Noise power in dBm.
    """
    kT = pow2dbm(thermal_noise(bandwidth, temperature))
    BW = pow2db(bandwidth)
    NF = noise_figure
    return kT + NF + BW
