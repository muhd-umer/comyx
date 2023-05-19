import numpy as np
from komm import PSKModulation

QPSK = PSKModulation(4, phase_offset=np.pi / 4)


def calculate_noma_rate(M, K, Pt_lin, alpha, gain_mat, noise_lin):
    """
    Calculates the sum rate of NOMA for a given set of parameters.

    Parameters:
    M (int): Number of users.
    K (int): Number of bits to be transmitted.
    Pt_lin (numpy.ndarray): Array of transmit power levels for each user.
    alpha (numpy.ndarray): Array of path loss coefficients for each user.
    gain_mat (numpy.ndarray): Matrix of channel gains between each user and the base station.
    noise_lin (float): Linear value of the noise power.

    Returns:
    numpy.ndarray: Array of sum rate values for each transmit power level.
    """
    if isinstance(Pt_lin, float):
        Pt_lin = [Pt_lin]

    rate_noma = np.zeros((M, K // 2))
    rate_noma_sum = np.zeros(len(Pt_lin))

    for u in range(len(Pt_lin)):
        rate_noma[0] = np.log2(
            1
            + Pt_lin[u]
            * alpha[0]
            * gain_mat[0]
            / (
                Pt_lin[u] * alpha[1] * gain_mat[0]
                + Pt_lin[u] * alpha[2] * gain_mat[0]
                + Pt_lin[u] * alpha[3] * gain_mat[0]
                + noise_lin
            )
        )  # User 1 (strongest user)
        rate_noma[1] = np.log2(
            1
            + Pt_lin[u]
            * alpha[1]
            * gain_mat[1]
            / (
                Pt_lin[u] * alpha[2] * gain_mat[1]
                + Pt_lin[u] * alpha[3] * gain_mat[1]
                + noise_lin
            )
        )  # User 2
        rate_noma[2] = np.log2(
            1
            + Pt_lin[u]
            * alpha[2]
            * gain_mat[2]
            / (Pt_lin[u] * alpha[3] * gain_mat[2] + noise_lin)
        )  # User 3
        rate_noma[3] = np.log2(
            1 + Pt_lin[u] * alpha[3] * gain_mat[3] / noise_lin
        )  # User 4 (weakest user)

        # Calculate the sum rate of NOMA by taking the mean of the rate of all users
        rate_noma_sum[u] = np.mean(rate_noma)

    return rate_noma_sum, rate_noma


def calculate_ofdma_rate(M, K, Pt_lin, gain_mat, noise_lin, beta_ofdma):
    """
    Calculates the rate of OFDMA for a given set of parameters.

    Parameters:
    M (int): Number of users.
    K (int): Number of bits to be transmitted.
    Pt_lin (numpy.ndarray): Array of transmit power levels for each user.
    gain_mat (numpy.ndarray): Matrix of channel gains between each user and the base station.
    noise_lin (float): Linear value of the noise power.
    beta_ofdma (float): Beta value for OFDMA.

    Returns:
    numpy.ndarray: Array of sum rate values for each transmit power level.
    """
    if isinstance(Pt_lin, float):
        Pt_lin = [Pt_lin]

    rate_ofdma = np.zeros((M, K // 2))
    rate_ofdma_sum = np.zeros(len(Pt_lin))

    for u in range(len(Pt_lin)):
        rate_ofdma[0] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[0] / noise_lin)
        rate_ofdma[1] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[1] / noise_lin)
        rate_ofdma[2] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[2] / noise_lin)
        rate_ofdma[3] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[3] / noise_lin)

        # Calculate the sum rate of OFDMA by taking the mean of the rate of all users
        rate_ofdma_sum[u] = np.mean(rate_ofdma)

    return rate_ofdma_sum, rate_ofdma


def noma_decoding(QPSK, M, K, Pt, alpha, gain_mat, noise_var, y_eq):
    """
    Perform decoding of signals in a NOMA system with four users.

    Args:
    QPSK (PSKModulation): QPSK modulation object.
    M (int): Number of users.
    K (int): Number of bits to be transmitted.
    Pt (ndarray): Transmit power in linear scale.
    alpha (ndarray): Path loss coefficients for each user.
    gain_mat (ndarray): Channel gain matrix.
    noise_var (float): Noise variance.
    y_eq (ndarray): Equalized received signal.

    Returns:
    x_hat (ndarray): Decoded symbols for each user.
    """
    x_hat = np.zeros((len(Pt), M, K), dtype=int)

    for i in range(len(Pt)):
        # Perform decoding of signal at user 1
        x_hat[i, 0] = QPSK.demodulate(y_eq[i, 0])  # Direct decoding

        # Perform decoding of signal at user 2
        u1_hat = QPSK.demodulate(y_eq[i, 1])  # Decode user 1 signal
        u1_remod = QPSK.modulate(u1_hat)  # Remodulate user 1 signal
        rem_u1 = y_eq[i, 1] - (np.sqrt(alpha[0] * Pt[i]) * u1_remod)
        x_hat[i, 1] = QPSK.demodulate(rem_u1)  # Decode user 2 signal

        # Perform decoding of signal at user 3
        u1_hat = QPSK.demodulate(y_eq[i, 2])  # Decode user 1 signal
        u1_remod = QPSK.modulate(u1_hat)  # Remodulate user 1 signal
        u2_hat = QPSK.demodulate(
            y_eq[i, 2] - (np.sqrt(alpha[0] * Pt[i]) * u1_remod)
        )  # Decode user 2 signal
        u2_remod = QPSK.modulate(u2_hat)  # Remodulate user 2 signal
        x_hat[i, 2] = QPSK.demodulate(
            y_eq[i, 2]
            - (np.sqrt(alpha[0] * Pt[i]) * u1_remod)
            - (np.sqrt(alpha[1] * Pt[i]) * u2_remod)
        )  # Decode user 3 signal

        # Perform decoding of signal at user 4
        u1_hat = QPSK.demodulate(y_eq[i, 3])  # Decode user 1 signal
        u1_remod = QPSK.modulate(u1_hat)  # Remodulate user 1 signal
        u2_hat = QPSK.demodulate(
            y_eq[i, 3] - (np.sqrt(alpha[0] * Pt[i]) * u1_remod)
        )  # Decode user 2 signal
        u2_remod = QPSK.modulate(u2_hat)  # Remodulate user 2 signal
        u3_hat = QPSK.demodulate(
            y_eq[i, 3]
            - (np.sqrt(alpha[0] * Pt[i]) * u1_remod)
            - (np.sqrt(alpha[1] * Pt[i]) * u2_remod)
        )  # Decode user 3 signal
        u3_remod = QPSK.modulate(u3_hat)  # Remodulate user 3 signal
        x_hat[i, 3] = QPSK.demodulate(
            y_eq[i, 3]
            - (np.sqrt(alpha[0] * Pt[i]) * u1_remod)
            - (np.sqrt(alpha[1] * Pt[i]) * u2_remod)
            - (np.sqrt(alpha[2] * Pt[i]) * u3_remod)
        )  # Decode user 4 signal

    return x_hat


def generate_qpsk_symbols(QPSK, M, K):
    """
    Generate QPSK symbols from random message bits for each user.

    Args:
    QPSK (PSKModulation): QPSK modulation object.
    M (int): Number of message bits.
    K (int): Number of users.

    Returns:
    x_qpsk (ndarray): QPSK symbols for each user.
    """

    # Generate random message bits for each user
    x = np.random.randint(0, 2, size=(M, K))

    # Convert the input bits to QPSK symbols
    x_qpsk = np.zeros((M, K // 2), dtype=complex)
    for i in range(M):
        x_qpsk[i] = QPSK.modulate(x[i])

    return x_qpsk
