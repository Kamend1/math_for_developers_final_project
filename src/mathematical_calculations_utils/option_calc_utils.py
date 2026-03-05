import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    This method takes the standard Black-Scholes formula in simple code using the cumulative density function
    from the scipy library
    S: Current Price, K: Strike, T: Time (yrs), r: Risk-free rate, sigma: Volatility
    """
    if T <= 0: return np.maximum(S - K, 0) if option_type == 'call' else np.maximum(K - S, 0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else: # Put option for portfolio protection (2_1)
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def calculate_option_derivatives(S, K, T, r, sigma, option_type='call'):
    """
    Calculates numerical derivatives for an option.
    """
    h = 0.0001
    
    # Calculate callable prices at three points
    p_center = black_scholes(S, K, T, r, sigma, option_type)
    p_plus = black_scholes(S + h, K, T, r, sigma, option_type)
    p_minus = black_scholes(S - h, K, T, r, sigma, option_type)
    
    # First Derivative (Slope)
    d1 = (p_plus - p_minus) / (2 * h)
    
    # Second Derivative (Curvature)
    d2 = (p_plus - 2 * p_center + p_minus) / (h**2)
    
    return p_center, d1, d2


def calculate_option_derivatives_1(S, K, T, r, sigma, option_type="put"):
    """
    Returns (price, delta, gamma) for Black–Scholes call/put.
    Delta is dPrice/dS and gamma is d^2Price/dS^2.
    """
    S = float(S)          # ensure float, not int
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)

    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be positive for Black–Scholes.")

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    elif option_type.lower() == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))  # <-- THIS SHOULD NOT BE 0

    return price, delta, gamma
    

def calculate_secondary_option_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Calculates Vega, Rho and Theta for a European option using the Black–Scholes model.

    Parameters
    ----------
    S : float or np.ndarray
        Underlying asset (portfolio) value.
    K : float
        Strike price.
    T : float
        Time to maturity (years).
    r : float
        Risk-free interest rate (continuous compounding).
    sigma : float
        Volatility of the underlying.
    option_type : str
        'call' or 'put'

    Returns
    -------
    vega, rho, theta
    """

    S = np.asarray(S, dtype=float)

    sqrtT = np.sqrt(T)

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    pdf_d1 = norm.pdf(d1)

    # --- Vega ---
    vega = S * pdf_d1 * sqrtT

    if option_type.lower() == "call":

        # --- Rho ---
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)

        # --- Theta ---
        theta = (
            -(S * pdf_d1 * sigma) / (2 * sqrtT)
            - r * K * np.exp(-r * T) * norm.cdf(d2)
        )

    elif option_type.lower() == "put":

        # --- Rho ---
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

        # --- Theta ---
        theta = (
            -(S * pdf_d1 * sigma) / (2 * sqrtT)
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
        )

    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return vega, rho, theta