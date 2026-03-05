import numpy as np
from . import option_calc_utils as o_calc


def calculate_bond_price(yield_to_maturity, face_value, coupon_rate, years, num_periods_year):
    """
    Calculates a single bond price for a given yield to maturity with predefined (semiannual) compounding. Calculated the sum of the present values of all coupon payments and the present value of the principal payment at maturity. The bond cash flows are discounted at the yield to maturity given to the method.  
    """
    periods = int(years * num_periods_year)
    semi_coupon = (face_value * coupon_rate) / num_periods_year
    semi_yield = yield_to_maturity / num_periods_year
    t = np.arange(1, periods + 1).reshape(-1, 1)
    
    pv_coupons = np.sum(semi_coupon / (1 + semi_yield)**t, axis=0)
    pv_face = face_value / (1 + semi_yield)**periods
    
    price = pv_coupons + pv_face
    
    return price


def calculate_callable_bond_price(yield_to_maturity, 
                                  face_value, 
                                  coupon_rate, 
                                  years, 
                                  num_periods_year, 
                                  strike, 
                                  risk_free=0.03, 
                                  volatility=0.06):
    """
    Calculates a single callable bond price for a given yield to maturity.
    """
    # Ensure these lines all start with exactly 4 spaces
    periods = int(years * num_periods_year)
    semi_coupon = (face_value * coupon_rate) / num_periods_year
    semi_yield = yield_to_maturity / num_periods_year
    
    # Check this line specifically for trailing spaces
    t = np.arange(1, periods + 1).reshape(-1, 1)
    
    pv_coupons = np.sum(semi_coupon / (1 + semi_yield)**t, axis=0)
    pv_face = face_value / (1 + semi_yield)**periods
    
    price = pv_coupons + pv_face
    
    # Ensure 'o_calc' is imported and accessible in this scope
    option_price = o_calc.black_scholes(price, strike, 1 / num_periods_year , risk_free, volatility)
    
    bond_price = price - option_price
    
    return bond_price

def calculate_derivatives(y0, face_v, coupon, years, num_periods):
    """
    Calculates the 1st and 2nd derivatives of the bond price function at y0.
    """
    h = 0.0001  # An infinitesimal change in yield
    
    # Calculate price at three points
    p_center = calculate_bond_price(y0, face_v, coupon, years, num_periods)
    p_plus = calculate_bond_price(y0 + h, face_v, coupon, years, num_periods)
    p_minus = calculate_bond_price(y0 - h, face_v, coupon, years, num_periods)
    
    # First Derivative (Slope / Dollar Duration)
    # f'(x) ≈ [f(x+h) - f(x-h)] / 2h
    d1 = (p_plus - p_minus) / (2 * h)
    
    # Second Derivative (Curvature / Dollar Convexity)
    # f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h^2
    d2 = (p_plus - 2 * p_center + p_minus) / (h**2)
    
    return p_center, d1, d2


def calculate_callable_derivatives(y0, face_v, coupon, years, num_periods, strike):
    """
    Calculates 1st and 2nd numerical derivatives of the callable bond price function at y0.
    """
    h = 0.0001
    
    # Calculate callable prices at three points
    p_center = calculate_callable_bond_price(y0, face_v, coupon, years, num_periods, strike)
    p_plus = calculate_callable_bond_price(y0 + h, face_v, coupon, years, num_periods, strike)
    p_minus = calculate_callable_bond_price(y0 - h, face_v, coupon, years, num_periods, strike)
    
    # First Derivative (Slope)
    d1 = (p_plus - p_minus) / (2 * h)
    
    # Second Derivative (Curvature)
    d2 = (p_plus - 2 * p_center + p_minus) / (h**2)
    
    return p_center, d1, d2


def draw_tangent_line(ytm_range, y0, p0, d1):
    """
    Calculates the Y-values for a tangent line at point (y0, p0).
    """
    # Linear approximation: P = P0 + slope * change_in_yield
    return p0 + d1 * (ytm_range - y0)


def draw_convex_line(ytm_range, y0, p0, d1, d2):
    """
    Calculates the Y-values for a convex line at point (y0, p0).
    """
    dy = ytm_range - y0
    
    # Quadratic (Convexity) - P = P0 + P'dy + 0.5 * P''dy^2
    return p0 + (d1 * dy) + (0.5 * d2 * dy**2)