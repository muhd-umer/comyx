import numpy as np


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

    C_noma = np.zeros((M, K // 2))
    C_noma_sum = np.zeros(len(Pt_lin))

    for u in range(len(Pt_lin)):
        C_noma[0] = np.log2(
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
        C_noma[1] = np.log2(
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
        C_noma[2] = np.log2(
            1
            + Pt_lin[u]
            * alpha[2]
            * gain_mat[2]
            / (Pt_lin[u] * alpha[3] * gain_mat[2] + noise_lin)
        )  # User 3
        C_noma[3] = np.log2(
            1 + Pt_lin[u] * alpha[3] * gain_mat[3] / noise_lin
        )  # User 4 (weakest user)

        # Calculate the sum rate of NOMA by taking the mean of the rate of all users
        C_noma_sum[u] = np.mean(C_noma)

    return C_noma_sum, C_noma


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

    C_ofdma = np.zeros((M, K // 2))
    C_ofdma_sum = np.zeros(len(Pt_lin))

    for u in range(len(Pt_lin)):
        C_ofdma[0] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[0] / noise_lin)
        C_ofdma[1] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[1] / noise_lin)
        C_ofdma[2] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[2] / noise_lin)
        C_ofdma[3] = beta_ofdma * np.log2(1 + Pt_lin[u] * gain_mat[3] / noise_lin)

        # Calculate the sum rate of OFDMA by taking the mean of the rate of all users
        C_ofdma_sum[u] = np.mean(C_ofdma)

    return C_ofdma_sum, C_ofdma
