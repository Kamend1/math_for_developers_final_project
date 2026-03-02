import numpy as np


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

def calculate_callable_bond_price(yield_to_maturity, face_value, coupon_rate, years, num_periods_year, strike, risk_free=0.03, volatility=0.06):
     """
    Calculates a single callable bond price for a given yield to maturity with predefined (semiannual) compounding. Calculated the sum of the present values of all coupon payments and the present value of the principal payment at maturity. The bond cash flows are discounted at the yield to maturity given to the method. This method calls a pre-defined black-scholes model method to calculate the value of the embedded call option. Returns the final callable bond price by subtracting the option price from the regular bond price. 
    """
    
    
    periods = int(years * num_periods_year)
    semi_coupon = (face_value * coupon_rate) / num_periods_year
    semi_yield = yield_to_maturity / num_periods_year
    t = np.arange(1, periods + 1).reshape(-1, 1)
    
    pv_coupons = np.sum(semi_coupon / (1 + semi_yield)**t, axis=0)
    pv_face = face_value / (1 + semi_yield)**periods

    price = pv_coupons + pv_face

    option_price = o_calc.black_scholes(price, strike, years, risk_free, volatility)

    bond_price = price - option_price

    return bond_price