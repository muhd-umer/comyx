import argparse
import os

import matplotlib.pyplot as plt
import mpmath as mpm
import numpy as np
import scipy as sp
import scipy.io as io
import sympy as sym
from colorama import Fore, Style
from config import constants, environment, setting
from scipy.special import gamma
from sympy import N as NEval
from sympy import meijerg

import simcomm.core.propagation as prop
from simcomm.core import Nakagami, get_rvs
from simcomm.core.propagation import get_noise_power, get_pathloss
from simcomm.utils import db2pow, dbm2pow, get_distance, pow2db, pow2dbm, qfunc


def main(N, link_option, custom_run, save_path):
    # Load the environment
    pathloss_cfg = environment["pathloss"]
    fading_cfg = environment["fading"]
    positions = environment["positions"]

    # Additional parameters
    BANDWIDTH = constants["BANDWIDTH"]  # Bandwidth in Hz
    TEMP = constants["TEMP"]  # Temperature in Kelvin
    FREQ = constants["FREQ"]  # Frequency of carrier signal in Hz
    SIGMA = constants["SIGMA"]  # Shadowing standard deviation in dB

    # Positions
    pos_BS1 = positions["BS1"]
    pos_BS2 = positions["BS2"]
    pos_RIS = positions["RIS"]
    pos_U1c = positions["U1c"]
    pos_U2c = positions["U2c"]
    pos_Uf = positions["Uf"]

    # Distance parameters
    ## BS1 specific distances
    distance_iR = get_distance(pos_BS1, pos_RIS, 3)
    distance_Rc = get_distance(pos_RIS, pos_U1c, 3)
    distance_ic = get_distance(pos_BS1, pos_U1c, 3)
    distance_if = get_distance(pos_BS1, pos_Uf, 3)

    ## BS2 specific distances
    distance_iR_hat = get_distance(pos_BS2, pos_RIS, 3)
    distance_if_hat = get_distance(pos_BS2, pos_Uf, 3)

    ## Common distances
    distance_Rf = get_distance(pos_RIS, pos_Uf, 3)
    distance_ic_prime = get_distance(pos_BS2, pos_U1c, 3)

    ## BS specific distances for U2
    distance_ic_u2 = get_distance(pos_BS2, pos_U2c, 3)
    distance_Rc_u2 = get_distance(pos_RIS, pos_U2c, 3)
    distance_ic_prime_u2 = get_distance(pos_BS1, pos_U2c, 3)

    # Simulation parameters
    K = 70
    N = 10000
    beta_r = 0.5
    beta_t = 0.5
    shape = (N, 1)
    shape_ris = (K // 2, N, 1)

    # Additional parameters
    BANDWIDTH = constants["BANDWIDTH"]  # Bandwidth in Hz
    TEMP = constants["TEMP"]  # Temperature in Kelvin
    FREQ = constants["FREQ"]  # Frequency of carrier signal in Hz
    SIGMA = constants["SIGMA"]  # Shadowing standard deviation in dB

    Pt = np.linspace(-40, 20, 121)  # Transmit power in dBm
    Pt_lin = dbm2pow(Pt)  # Transmit power in linear scale
    N0 = get_noise_power(BANDWIDTH, TEMP, 12)  # Noise power in dBm
    N0_lin = dbm2pow(N0)  # Noise power in linear scale

    # Power allocation
    zeta_ic = 0.3
    zeta_if = 0.7
    zeta_ic_hat = 0.3
    zeta_if_hat = 0.7

    rho = Pt_lin / N0_lin  # SNR

    # Scaling factors
    scale_ic = np.zeros_like(rho)
    scale_ic_prime = np.linspace(0.001, 1.4, len(rho) - 20)
    scale_ic[20:] = scale_ic_prime
    scale_f = np.linspace(0.01, 0.15, len(rho))

    # Pathloss computations
    pathloss_iR = get_pathloss(
        **pathloss_cfg["ris"], distance=distance_iR, frequency=FREQ
    )
    pathloss_Rc = get_pathloss(
        **pathloss_cfg["risC"], distance=distance_Rc, frequency=FREQ
    )
    pathloss_ic = get_pathloss(
        **pathloss_cfg["center"], distance=distance_ic, frequency=FREQ
    )
    pathloss_ic_prime = get_pathloss(
        **pathloss_cfg["inter"], distance=distance_ic_prime, frequency=FREQ
    )
    pathloss_ic_u2 = get_pathloss(
        **pathloss_cfg["center"], distance=distance_ic_u2, frequency=FREQ
    )
    pathloss_ic_prime_u2 = get_pathloss(
        **pathloss_cfg["inter"], distance=distance_ic_prime_u2, frequency=FREQ
    )
    pathloss_Rc_u2 = get_pathloss(
        **pathloss_cfg["risC"], distance=distance_Rc_u2, frequency=FREQ
    )
    pathloss_if = get_pathloss(
        **pathloss_cfg["edge"], distance=distance_if, frequency=FREQ
    )
    pathloss_iR_hat = get_pathloss(
        **pathloss_cfg["ris"], distance=distance_iR_hat, frequency=FREQ
    )
    pathloss_if_hat = get_pathloss(
        **pathloss_cfg["edge"], distance=distance_if_hat, frequency=FREQ
    )
    pathloss_Rf = get_pathloss(
        **pathloss_cfg["risE"], distance=distance_Rf, frequency=FREQ
    )

    # Fading samples
    samples_iR = get_rvs(**fading_cfg["nakagami-d"], shape=shape_ris)
    samples_Rc = get_rvs(**fading_cfg["nakagami-d"], shape=shape_ris)
    samples_ic = get_rvs(**fading_cfg["nakagami-id"], shape=shape)
    samples_ic_prime = get_rvs(**fading_cfg["nakagami-id"], shape=shape)

    samples_if = get_rvs(**fading_cfg["nakagami-id"], shape=shape)
    samples_iR_hat = get_rvs(**fading_cfg["nakagami-d"], shape=shape_ris)
    samples_if_hat = get_rvs(**fading_cfg["nakagami-id"], shape=shape)
    samples_Rf = get_rvs(**fading_cfg["nakagami-d"], shape=shape_ris)

    # Channel generation
    h_iR = np.abs(np.sqrt(db2pow(-1 * pathloss_iR)) * samples_iR)
    h_Rc = np.abs(np.sqrt(db2pow(-1 * pathloss_Rc)) * samples_Rc)
    h_ic = np.abs(np.sqrt(db2pow(-1 * pathloss_ic)) * samples_ic)
    h_ic_prime = np.abs(np.sqrt(db2pow(-1 * pathloss_ic_prime)) * samples_ic_prime)
    h_if = np.abs(np.sqrt(db2pow(-1 * pathloss_if)) * samples_if)
    h_iR_hat = np.abs(np.sqrt(db2pow(-1 * pathloss_iR_hat)) * samples_iR_hat)
    h_if_hat = np.abs(np.sqrt(db2pow(-1 * pathloss_if_hat)) * samples_if_hat)
    h_Rf = np.abs(np.sqrt(db2pow(-1 * pathloss_Rf)) * samples_Rf)
    h_ic_u2 = np.abs(np.sqrt(db2pow(-1 * pathloss_ic_u2)) * samples_ic)
    h_ic_prime_u2 = np.abs(
        np.sqrt(db2pow(-1 * pathloss_ic_prime_u2)) * samples_ic_prime
    )
    h_Rc_u2 = np.abs(np.sqrt(db2pow(-1 * pathloss_Rc_u2)) * samples_Rc)

    cascaded_ic = np.sum(h_iR * h_Rc, axis=0) * np.sqrt(beta_r)
    H_ic = cascaded_ic + h_ic

    cascaded_if = np.sum(h_iR * h_Rf, axis=0) * np.sqrt(beta_t)
    cascaded_if_hat = np.sum(h_iR_hat * h_Rf, axis=0) * np.sqrt(beta_t)
    H_if = cascaded_if + h_if
    H_if_hat = cascaded_if_hat + h_if_hat

    cascaded_ic_u2 = np.sum(h_iR_hat * h_Rc_u2, axis=0) * np.sqrt(beta_r)
    H_ic_u2 = cascaded_ic_u2 + h_ic_u2

    ## PDF of SINR $\gamma_{i,c\rightarrow f}$
    # Effective Channel $\textbf{H}_{i, c}=\textbf{h}_{i, c}+\textbf{h}_{R, c}^H \mathbf{\Theta_r}\textbf{h}_{i, R}$
    # Channel Gain $Z_{i,c} = |H_{i,c}|^2 = (h_{i,c} + G_{i,R,c})^2$
    # Direct Channel $h_{i,c}$

    m_ic = fading_cfg["nakagami-id"]["m"]
    omega_ic = fading_cfg["nakagami-id"]["omega"] * db2pow(-1 * pathloss_ic)
    omega_ic_prime = fading_cfg["nakagami-id"]["omega"] * db2pow(-1 * pathloss_ic_prime)

    omega_ic_u2 = fading_cfg["nakagami-id"]["omega"] * db2pow(-1 * pathloss_ic_u2)
    omega_ic_prime_u2 = fading_cfg["nakagami-id"]["omega"] * db2pow(
        -1 * pathloss_ic_prime_u2
    )

    def fun_mu_h_ic(p, m_ic, omega_ic):
        return (gamma(m_ic + p / 2) / gamma(m_ic)) * (m_ic / omega_ic) ** (-p / 2)

    mu_h_ic = fun_mu_h_ic(1, m_ic, omega_ic)  # 1st moment of h_ic
    mu_h_ic_2 = fun_mu_h_ic(2, m_ic, omega_ic)  # 2nd moment of h_ic

    mu_h_ic_u2 = fun_mu_h_ic(1, m_ic, omega_ic_u2)  # 1st moment of h_ic
    mu_h_ic_2_u2 = fun_mu_h_ic(2, m_ic, omega_ic_u2)  # 2nd moment of h_ic

    k_h_ic = (mu_h_ic**2) / (mu_h_ic_2 - mu_h_ic**2)  # Shape parameter of h_ic
    theta_h_ic = (mu_h_ic_2 - mu_h_ic**2) / mu_h_ic  # Scale parameter of h_ic

    k_h_ic_u2 = (mu_h_ic_u2**2) / (
        mu_h_ic_2_u2 - mu_h_ic_u2**2
    )  # Shape parameter of h_ic
    theta_h_ic_u2 = (
        mu_h_ic_2_u2 - mu_h_ic_u2**2
    ) / mu_h_ic_u2  # Scale parameter of h_ic

    # Cascaded Channel $G_{i,R,c} = \sqrt{\beta_r} \sum_{k=1}^{K} |{h_{R,c}}||{h_{i,R}}|$
    m_iR = fading_cfg["nakagami-d"]["m"]
    m_Rc = fading_cfg["nakagami-d"]["m"]
    omega_iR = fading_cfg["nakagami-d"]["omega"] * db2pow(-1 * pathloss_iR)
    omega_Rc = fading_cfg["nakagami-d"]["omega"] * db2pow(-1 * pathloss_Rc)
    omega_Rc_u2 = fading_cfg["nakagami-d"]["omega"] * db2pow(-1 * pathloss_Rc_u2)

    def fun_mu_h_Rc(p, m_Rc, omega_Rc):
        return gamma(m_Rc + p / 2) / gamma(m_Rc) * (m_Rc / omega_Rc) ** (-p / 2)

    def fun_mu_G_iRc(p, m_iR, omega_iR, m_Rc, omega_Rc, K, beta_r):
        return (
            gamma(m_Rc + (p / 2))
            * (np.sqrt(beta_r) * K) ** p
            * gamma(m_iR + (p / 2))
            * ((m_iR * m_Rc) / (omega_iR * omega_Rc)) ** (-p / 2)
        ) / (gamma(m_iR) * gamma(m_Rc))

    mu_G_iRc = fun_mu_G_iRc(
        1, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r
    )  # 1st moment of G_iRc
    mu_G_iRc_2 = fun_mu_G_iRc(
        2, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r
    )  # 2nd moment of G_iRc

    mu_G_iRc_u2 = fun_mu_G_iRc(
        1, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r
    )  # 1st moment of G_iRc
    mu_G_iRc_2_u2 = fun_mu_G_iRc(
        2, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r
    )  # 2nd moment of G_iRc

    k_G_iRc = mu_G_iRc**2 / (mu_G_iRc_2 - mu_G_iRc**2)  # Shape parameter of G_iRc
    theta_G_iRc = (mu_G_iRc_2 - mu_G_iRc**2) / mu_G_iRc  # Scale parameter of G_iRc

    k_G_iRc_u2 = mu_G_iRc_u2**2 / (
        mu_G_iRc_2_u2 - mu_G_iRc_u2**2
    )  # Shape parameter of G_iRc
    theta_G_iRc_u2 = (
        mu_G_iRc_2_u2 - mu_G_iRc_u2**2
    ) / mu_G_iRc_u2  # Scale parameter of G_iRc

    # Effective Channel Gain $Z_{i,c} = |H_{i,c}|^2 = (h_{i,c} + G_{i,R,c})^2$
    mu_Z_ic = (
        fun_mu_G_iRc(2, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r)
        + fun_mu_h_ic(2, m_ic, omega_ic)
        + (
            2
            * fun_mu_G_iRc(1, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r)
            * fun_mu_h_ic(1, m_ic, omega_ic)
        )
    )

    mu_Z_ic_2 = (
        fun_mu_G_iRc(4, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r)
        + fun_mu_h_ic(4, m_ic, omega_ic)
        + (
            6
            * fun_mu_G_iRc(2, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r)
            * fun_mu_h_ic(2, m_ic, omega_ic)
        )
        + (
            4
            * fun_mu_h_ic(3, m_ic, omega_ic)
            * fun_mu_G_iRc(1, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r)
        )
        + (
            4
            * fun_mu_h_ic(1, m_ic, omega_ic)
            * fun_mu_G_iRc(3, m_iR, omega_iR, m_Rc, omega_Rc, K // 2, beta_r)
        )
    )

    mu_Z_ic_u2 = (
        fun_mu_G_iRc(2, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r)
        + fun_mu_h_ic(2, m_ic, omega_ic_u2)
        + (
            2
            * fun_mu_G_iRc(1, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r)
            * fun_mu_h_ic(1, m_ic, omega_ic_u2)
        )
    )

    mu_Z_ic_2_u2 = (
        fun_mu_G_iRc(4, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r)
        + fun_mu_h_ic(4, m_ic, omega_ic_u2)
        + (
            6
            * fun_mu_G_iRc(2, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r)
            * fun_mu_h_ic(2, m_ic, omega_ic_u2)
        )
        + (
            4
            * fun_mu_h_ic(3, m_ic, omega_ic_u2)
            * fun_mu_G_iRc(1, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r)
        )
        + (
            4
            * fun_mu_h_ic(1, m_ic, omega_ic_u2)
            * fun_mu_G_iRc(3, m_iR, omega_iR, m_Rc, omega_Rc_u2, K // 2, beta_r)
        )
    )

    k_Z_ic = mu_Z_ic**2 / (mu_Z_ic_2 - mu_Z_ic**2)  # Shape parameter of Z_ic
    theta_Z_ic = (mu_Z_ic_2 - mu_Z_ic**2) / mu_Z_ic  # Scale parameter of Z_ic

    k_Z_ic_u2 = mu_Z_ic_u2**2 / (
        mu_Z_ic_2_u2 - mu_Z_ic_u2**2
    )  # Shape parameter of Z_ic
    theta_Z_ic_u2 = (
        mu_Z_ic_2_u2 - mu_Z_ic_u2**2
    ) / mu_Z_ic_u2  # Scale parameter of Z_ic

    # $\mathcal{V_{i,c,f}} = {\zeta_{i,f}\rho|\textbf{H}_{i,c}|^2},$
    # where $\rho = \frac{P}{\sigma^2}$

    simulation_V_icf = zeta_if * rho * H_ic**2
    simulation_V_icf_u2 = zeta_if * rho * H_ic_u2**2

    k_V_icf = k_Z_ic * np.ones_like(rho)
    theta_V_icf = theta_Z_ic * zeta_if * rho

    k_V_icf_u2 = k_Z_ic_u2 * np.ones_like(rho)
    theta_V_icf_u2 = theta_Z_ic_u2 * zeta_if * rho

    # $\mathcal{B_{i,c,f}} = {\zeta_{i,c}\rho|\textbf{H}_{i,c}|^2 + \rho|\textbf{h}_{i,c^\prime}|^2 +  1}$
    # $\mathcal{B_{i,c,f}} = {\mathcal{W_{i,c}} +  1}$,
    # where $\mathcal{W_{i,c,f}} = \zeta_{i,c}\rho|\textbf{H}_{i,c}|^2 + \rho|\textbf{h}_{i,c^\prime}|^2$

    simulation_W_icf = (zeta_ic * rho * H_ic**2) + (rho * h_ic_prime**2)
    simulation_B_icf = simulation_W_icf + 1

    simulation_W_icf_u2 = (zeta_ic * rho * H_ic_u2**2) + (rho * h_ic_prime_u2**2)
    simulation_B_icf_u2 = simulation_W_icf_u2 + 1

    # $\mu _{\mathcal{W}_{ic}} = \rho  \mu _{h_{ic}}+\zeta  \rho  \mu _{Z_{ic}}$
    # $\mu _{\mathcal{W}_{ic}}^{(2)} = \rho ^2 \left(\zeta  \left(2 \mu _{h_{ic}} \mu
    #    _{Z_{ic}}+\zeta  \mu _{Z_{\text{ic2}}}\right)+\mu
    #    _{h_{\text{ic2}}}\right)$

    def fun_mu_h_ic_sqr_interf(p, m_ic, omega_ic):
        return (gamma(m_ic + p) / gamma(m_ic)) * (m_ic / omega_ic) ** (-p)

    mu_W_icf = (
        rho * fun_mu_h_ic_sqr_interf(1, m_ic, omega_ic_prime) + zeta_ic * rho * mu_Z_ic
    )  # 1st moment of W_ic

    mu_W_icf_2 = rho**2 * (
        zeta_ic
        * (
            (2 * fun_mu_h_ic_sqr_interf(1, m_ic, omega_ic_prime) * mu_Z_ic)
            + zeta_ic * mu_Z_ic_2
        )
        + fun_mu_h_ic_sqr_interf(2, m_ic, omega_ic_prime)
    )  # 2nd moment of W_ic

    mu_W_icf_u2 = (
        rho * fun_mu_h_ic_sqr_interf(1, m_ic, omega_ic_prime_u2)
        + zeta_ic * rho * mu_Z_ic_u2
    )  # 1st moment of W_ic

    mu_W_icf_2_u2 = rho**2 * (
        zeta_ic
        * (
            (2 * fun_mu_h_ic_sqr_interf(1, m_ic, omega_ic_prime_u2) * mu_Z_ic_u2)
            + zeta_ic * mu_Z_ic_2_u2
        )
        + fun_mu_h_ic_sqr_interf(2, m_ic, omega_ic_prime_u2)
    )  # 2nd moment of W_ic

    k_W_icf = mu_W_icf**2 / (mu_W_icf_2 - mu_W_icf**2)  # Shape parameter of W_ic
    theta_W_icf = (mu_W_icf_2 - mu_W_icf**2) / mu_W_icf  # Scale parameter of W_ic

    k_W_icf_u2 = mu_W_icf_u2**2 / (
        mu_W_icf_2_u2 - mu_W_icf_u2**2
    )  # Shape parameter of W_ic
    theta_W_icf_u2 = (
        mu_W_icf_2_u2 - mu_W_icf_u2**2
    ) / mu_W_icf_u2  # Scale parameter of W_ic

    mu_B_icf = mu_W_icf + 1  # 1st moment of B_icf
    mu_B_icf_2 = mu_W_icf_2 + 2 * mu_W_icf + 1  # 2nd moment of B_icf

    mu_B_icf_u2 = mu_W_icf_u2 + 1  # 1st moment of B_icf
    mu_B_icf_2_u2 = mu_W_icf_2_u2 + 2 * mu_W_icf_u2 + 1  # 2nd moment of B_icf

    k_B_icf = mu_B_icf**2 / (mu_B_icf_2 - mu_B_icf**2)  # Shape parameter of B_icf
    theta_B_icf = (mu_B_icf_2 - mu_B_icf**2) / mu_B_icf  # Scale parameter of B_icf

    k_B_icf_u2 = mu_B_icf_u2**2 / (
        mu_B_icf_2_u2 - mu_B_icf_u2**2
    )  # Shape parameter of B_icf
    theta_B_icf_u2 = (
        mu_B_icf_2_u2 - mu_B_icf_u2**2
    ) / mu_B_icf_u2  # Scale parameter of B_icf

    simulation_SINR_icf = simulation_V_icf / simulation_B_icf
    simulation_SINR_icf_u2 = simulation_V_icf_u2 / simulation_B_icf_u2

    def generalized_beta_prime_pdf(x, a, b, p, q):
        return (p * ((x / q) ** (a * p - 1)) * (1 + (x / q) ** p) ** (-a - b)) / (
            q * sp.special.beta(a, b)
        )

    def hypergeometric_f1_regularized(a, b, c):
        return sp.special.hyp1f1(a, b, c) / sp.special.gamma(b)

    # ### PDF of SINR $\gamma_{i,c}$

    # $\mathcal{V_{i,c}} = {\zeta_{i,c}\rho|\textbf{H}_{i,c}|^2},$
    #
    # where $\rho = \frac{P}{\sigma^2}$

    simulation_V_ic = zeta_ic * rho * H_ic**2
    simulation_V_ic_u2 = zeta_ic * rho * H_ic_u2**2

    k_V_ic = k_Z_ic * np.ones_like(rho)
    theta_V_ic = theta_Z_ic * zeta_ic * rho

    k_V_ic_u2 = k_Z_ic_u2 * np.ones_like(rho)
    theta_V_ic_u2 = theta_Z_ic_u2 * zeta_ic * rho

    # $\mathcal{B_{i,c}} = {\rho|\textbf{h}_{i,c^\prime}|^2 +  1}$
    #
    # $\mathcal{B_{i,c}} = {\mathcal{W_{i,c}} +  1}$,
    #
    # where $\mathcal{W_{i,c}} = \rho|\textbf{h}_{i,c^\prime}|^2$

    simulation_B_ic = (rho * h_ic_prime**2) + 1
    simulation_B_ic_u2 = (rho * h_ic_prime_u2**2) + 1

    mu_W_ic = rho * fun_mu_h_ic_sqr_interf(
        1, m_ic, omega_ic_prime
    )  # 1st moment of W_ic
    mu_W_ic_2 = rho**2 * fun_mu_h_ic_sqr_interf(
        2, m_ic, omega_ic_prime
    )  # 2nd moment of W_ic

    mu_W_ic_u2 = rho * fun_mu_h_ic_sqr_interf(
        1, m_ic, omega_ic_prime_u2
    )  # 1st moment of W_ic
    mu_W_ic_2_u2 = rho**2 * fun_mu_h_ic_sqr_interf(
        2, m_ic, omega_ic_prime_u2
    )  # 2nd moment of W_ic

    k_W_ic = mu_W_ic**2 / (mu_W_ic_2 - mu_W_ic**2)  # Shape parameter of W_ic
    theta_W_ic = (mu_W_ic_2 - mu_W_ic**2) / mu_W_ic  # Scale parameter of W_ic

    k_W_ic_u2 = mu_W_ic_u2**2 / (
        mu_W_ic_2_u2 - mu_W_ic_u2**2
    )  # Shape parameter of W_ic
    theta_W_ic_u2 = (
        mu_W_ic_2_u2 - mu_W_ic_u2**2
    ) / mu_W_ic_u2  # Scale parameter of W_ic

    mu_B_ic = mu_W_ic + 1  # 1st moment of B_ic
    mu_B_ic_2 = mu_W_ic_2 + 2 * mu_W_ic + 1  # 2nd moment of B_ic

    mu_B_ic_u2 = mu_W_ic_u2 + 1  # 1st moment of B_ic
    mu_B_ic_2_u2 = mu_W_ic_2_u2 + 2 * mu_W_ic_u2 + 1  # 2nd moment of B_ic

    k_B_ic = mu_B_ic**2 / (mu_B_ic_2 - mu_B_ic**2)  # Shape parameter of B_ic
    theta_B_ic = (mu_B_ic_2 - mu_B_ic**2) / mu_B_ic  # Scale parameter of B_ic

    k_B_ic_u2 = mu_B_ic_u2**2 / (
        mu_B_ic_2_u2 - mu_B_ic_u2**2
    )  # Shape parameter of B_ic
    theta_B_ic_u2 = (
        mu_B_ic_2_u2 - mu_B_ic_u2**2
    ) / mu_B_ic_u2  # Scale parameter of B_ic

    simulation_SINR_ic = simulation_V_ic / simulation_B_ic
    simulation_SINR_ic_u2 = simulation_V_ic_u2 / simulation_B_ic_u2

    ### PDF of SINR $\gamma_{f}$
    # Effective Channel $\textbf{H}_{i, f}=\textbf{h}_{i, f}+\textbf{h}_{R, f}^H \mathbf{\Theta_r}\textbf{h}_{i, R}$
    # Channel Gain $Z_{i,f} = |H_{i,f}|^2 = (h_{i,f} + G_{i,R,f})^2$
    # Direct Channel $h_{i,f}$
    # Additionally, $\hat{i} \in \mathcal{I}_c \backslash i$

    m_if = fading_cfg["nakagami-id"]["m"]
    m_if_hat = fading_cfg["nakagami-id"]["m"]
    omega_if = fading_cfg["nakagami-id"]["omega"] * db2pow(-1 * pathloss_if)
    omega_if_hat = fading_cfg["nakagami-id"]["omega"] * db2pow(-1 * pathloss_if_hat)

    def fun_mu_h_if(p, m_if, omega_if):
        return (gamma(m_if + p / 2) / gamma(m_if)) * (m_if / omega_if) ** (-p / 2)

    mu_h_if = fun_mu_h_if(1, m_if, omega_if)  # 1st moment of h_if
    mu_h_if_2 = fun_mu_h_if(2, m_if, omega_if)  # 2nd moment of h_if
    mu_h_if_hat = fun_mu_h_if(1, m_if_hat, omega_if_hat)  # 1st moment of h_if_hat
    mu_h_if_hat_2 = fun_mu_h_if(2, m_if_hat, omega_if_hat)  # 2nd moment of h_if_hat

    k_h_if = (mu_h_if**2) / (mu_h_if_2 - mu_h_if**2)  # Shape parameter of h_if
    theta_h_if = (mu_h_if_2 - mu_h_if**2) / mu_h_if  # Scale parameter of h_if

    k_h_if_hat = (mu_h_if_hat**2) / (
        mu_h_if_hat_2 - mu_h_if_hat**2
    )  # Shape parameter of h_if_hat
    theta_h_if_hat = (
        mu_h_if_hat_2 - mu_h_if_hat**2
    ) / mu_h_if_hat  # Scale parameter of h_if_hat

    # Cascaded Channel $G_{i,R,f} = \sqrt{\beta_t} \sum_{k=1}^{K} |{h_{R,f}}||{h_{i,R}}|$
    m_iR = fading_cfg["nakagami-d"]["m"]
    m_iR_hat = fading_cfg["nakagami-d"]["m"]
    m_Rf = fading_cfg["nakagami-d"]["m"]
    omega_iR = fading_cfg["nakagami-d"]["omega"] * db2pow(-1 * pathloss_iR)
    omega_iR_hat = fading_cfg["nakagami-d"]["omega"] * db2pow(-1 * pathloss_iR_hat)
    omega_Rf = fading_cfg["nakagami-d"]["omega"] * db2pow(-1 * pathloss_Rf)

    def fun_mu_G_iRf(p, m_iR, omega_iR, m_Rf, omega_Rf, K, beta_t):
        return (
            gamma(m_Rf + (p / 2))
            * (np.sqrt(beta_t) * K) ** p
            * gamma(m_iR + (p / 2))
            * ((m_iR * m_Rf) / (omega_iR * omega_Rf)) ** (-p / 2)
        ) / (gamma(m_iR) * gamma(m_Rf))

    mu_G_iRf = fun_mu_G_iRf(
        1, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t
    )  # 1st moment of G_iRc
    mu_G_iRf_2 = fun_mu_G_iRf(
        2, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t
    )  # 2nd moment of G_iRc

    mu_G_iRf_hat = fun_mu_G_iRf(
        1, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t
    )  # 1st moment of G_iRc
    mu_G_iRf_hat_2 = fun_mu_G_iRf(
        2, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t
    )  # 2nd moment of G_iRcarameter of G_iRc

    k_G_iRf = mu_G_iRf**2 / (mu_G_iRf_2 - mu_G_iRf**2)  # Shape parameter of G_iRc
    theta_G_iRf = (mu_G_iRf_2 - mu_G_iRf**2) / mu_G_iRf  # Scale parameter of G_iRc

    k_G_iRf_hat = mu_G_iRf_hat**2 / (
        mu_G_iRf_hat_2 - mu_G_iRf_hat**2
    )  # Shape parameter of G_iRc
    theta_G_iRf_hat = (
        mu_G_iRf_hat_2 - mu_G_iRf_hat**2
    ) / mu_G_iRf_hat  # Scale parameter of G_iRc

    # Effective Channel Gain $Z_{i,f} = |H_{i,f}|^2 = (h_{i,f} + G_{i,R,f})^2$
    mu_Z_if = (
        fun_mu_G_iRf(2, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t)
        + fun_mu_h_if(2, m_if, omega_if)
        + (
            2
            * fun_mu_G_iRf(1, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t)
            * fun_mu_h_if(1, m_if, omega_if)
        )
    )

    mu_Z_if_2 = (
        fun_mu_G_iRf(4, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t)
        + fun_mu_h_if(4, m_if, omega_if)
        + (
            6
            * fun_mu_G_iRf(2, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t)
            * fun_mu_h_if(2, m_if, omega_if)
        )
        + (
            4
            * fun_mu_h_if(3, m_if, omega_if)
            * fun_mu_G_iRf(1, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t)
        )
        + (
            4
            * fun_mu_h_if(1, m_if, omega_if)
            * fun_mu_G_iRf(3, m_iR, omega_iR, m_Rf, omega_Rf, K // 2, beta_t)
        )
    )

    mu_Z_if_hat = (
        fun_mu_G_iRf(2, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t)
        + fun_mu_h_if(2, m_if_hat, omega_if_hat)
        + (
            2
            * fun_mu_G_iRf(1, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t)
            * fun_mu_h_if(1, m_if_hat, omega_if_hat)
        )
    )

    mu_Z_if_hat_2 = (
        fun_mu_G_iRf(4, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t)
        + fun_mu_h_if(4, m_if_hat, omega_if_hat)
        + (
            6
            * fun_mu_G_iRf(2, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t)
            * fun_mu_h_if(2, m_if_hat, omega_if_hat)
        )
        + (
            4
            * fun_mu_h_if(3, m_if_hat, omega_if_hat)
            * fun_mu_G_iRf(1, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t)
        )
        + (
            4
            * fun_mu_h_if(1, m_if_hat, omega_if_hat)
            * fun_mu_G_iRf(3, m_iR_hat, omega_iR_hat, m_Rf, omega_Rf, K // 2, beta_t)
        )
    )

    k_Z_if = mu_Z_if**2 / (mu_Z_if_2 - mu_Z_if**2)  # Shape parameter of Z_if
    theta_Z_if = (mu_Z_if_2 - mu_Z_if**2) / mu_Z_if  # Scale parameter of Z_if

    k_Z_if_hat = mu_Z_if_hat**2 / (
        mu_Z_if_hat_2 - mu_Z_if_hat**2
    )  # Shape parameter of Z_if_hat
    theta_Z_if_hat = (
        mu_Z_if_hat_2 - mu_Z_if_hat**2
    ) / mu_Z_if_hat  # Scale parameter of Z_if_hat

    # $\mathcal{V}_{f}=\zeta_{i,f}\rho|\textbf{H}_{i, f}|^2 + \zeta_{i',f}\rho|\textbf{H}_{i', f}|^2$
    simulation_V_f = zeta_if * rho * H_if**2 + zeta_if_hat * rho * H_if_hat**2

    mu_V_f = (zeta_if * rho * mu_Z_if) + (
        zeta_if_hat * rho * mu_Z_if_hat
    )  # 1st moment of V_f

    mu_V_f_2 = rho**2 * (
        (zeta_if * k_Z_if * theta_Z_if) ** 2
        + (zeta_if_hat**2 * k_Z_if_hat * (1 + k_Z_if_hat) * theta_Z_if_hat**2)
        + (
            zeta_if
            * k_Z_if
            * theta_Z_if
            * (zeta_if * theta_Z_if + 2 * zeta_if_hat * k_Z_if_hat * theta_Z_if_hat)
        )
    )  # 2nd moment of V_f

    k_V_f = mu_V_f**2 / (mu_V_f_2 - mu_V_f**2)  # Shape parameter of V_f
    theta_V_f = (mu_V_f_2 - mu_V_f**2) / mu_V_f  # Scale parameter of V_f

    # $\mathcal{B}_{f}=\zeta_{i,c}\rho|\textbf{H}_{i, f}|^2 + \zeta_{i',c}\rho|\textbf{H}_{i', f}|^2 + 1$
    # $\mathcal{B}_{f}=\mathcal{W}_{f} + 1$
    # $\mathcal{W}_{f}=\zeta_{i,c}\rho|\textbf{H}_{i, f}|^2 + \zeta_{i',c}\rho|\textbf{H}_{i', f}|^2$

    simulation_W_f = zeta_ic * rho * H_if**2 + zeta_ic_hat * rho * H_if_hat**2
    simulation_B_f = simulation_W_f + 1

    mu_W_f = (zeta_ic * rho * mu_Z_if) + (
        zeta_ic_hat * rho * mu_Z_if_hat
    )  # 1st moment of W_f

    mu_W_f_2 = rho**2 * (
        (zeta_ic * k_Z_if * theta_Z_if) ** 2
        + (zeta_ic_hat**2 * k_Z_if_hat * (1 + k_Z_if_hat) * theta_Z_if_hat**2)
        + (
            zeta_ic
            * k_Z_if
            * theta_Z_if
            * (zeta_ic * theta_Z_if + 2 * zeta_ic_hat * k_Z_if_hat * theta_Z_if_hat)
        )
    )  # 2nd moment of W_f

    k_W_f = mu_W_f**2 / (mu_W_f_2 - mu_W_f**2)  # Shape parameter of W_f
    theta_W_f = (mu_W_f_2 - mu_W_f**2) / mu_W_f  # Scale parameter of W_f

    mu_B_f = mu_W_f + 1  # 1st moment of B_f
    mu_B_f_2 = mu_W_f_2 + 2 * mu_W_f + 1  # 2nd moment of B_f

    k_B_f = mu_B_f**2 / (mu_B_f_2 - mu_B_f**2)  # Shape parameter of B_f
    theta_B_f = (mu_B_f_2 - mu_B_f**2) / mu_B_f  # Scale parameter of B_f

    simulation_SINR_f = simulation_V_f / simulation_B_f

    ## Ergodic Rates
    # $\mathcal{R(k,m,\theta,\Omega)}=\frac{1}{\Omega  \log (2) \Gamma (k) \Gamma (m)}{\pi  \csc (\pi  m) \left(\Omega  \Gamma (k+m) B_{\frac{\theta}{\Omega }}(m,-k-m+1)-\theta  k \Gamma (k) _3\tilde{F}_2\left(1,1,k+1;2,2-m;\frac{\theta }{\Omega}\right)\right)}$

    def rate_meijerg(k, m, theta, omega):
        return (1 / (mpm.log(2) * mpm.beta(k, m) * mpm.gamma(k + m))) * mpm.meijerg(
            [[0, 1 - m], [1]], [[0, 0, k], []], mpm.mpf(omega) / mpm.mpf(theta)
        )

    print(f"{Fore.CYAN}Done!{Style.RESET_ALL}")

    if save_path != "":
        if not custom_run:
            res_file = os.path.join(save_path, f"results_{link_option}.mat")
        else:
            res_file = os.path.join(save_path, f"results_{link_option}_custom.mat")

        tx_power = os.path.join(save_path, f"tx_power_dB.mat")

        # Save the results
        io.savemat(
            res_file,
            {},
        )
        io.savemat(tx_power, {"tx_power": Pt})

        print(f"{Fore.YELLOW}Results saved to: './{res_file}'{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}Skipping results.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate a wireless network with three users and two base stations."
    )
    parser.add_argument(
        "--realizations",
        type=int,
        default=10000,
        help="Number of channel realizations",
    )
    parser.add_argument(
        "--setting",
        type=str,
        default="ris32",
        choices=setting.keys(),
        help="Link option",
    )
    parser.add_argument(
        "--custom",
        action="store_true",
        help="Whether to use custom power allocation",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Skip saving results to .mat files",
    )

    args = parser.parse_args()
    if not args.no_save:
        os.makedirs("results", exist_ok=True)
        save_path = "results/"
    else:
        save_path = ""

    main(args.realizations, args.setting, args.custom, save_path)
