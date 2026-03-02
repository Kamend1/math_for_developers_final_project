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

