import numpy as np

def generate_portfolio_weights(n):
    """
    This method receives an argument such as a number e.g. 5 and creates this many random numbers in a list.
    Afterwards each of the n numbers is divided by the sum of all numbers so that the sum of all numbers is
    equal to 1. This is simulates portfolio weights in a stock portfolio consisting of n stocks.
    """
    weights = []
    weights = np.random.random(n)
    weights = weights / np.sum(weights)
    return weights


def simulation_engine(weights, annual_returns, annual_cov_matrix, risk_free_rate):
    # Calculate Expected Portfolio Return (w^T * μ)
    port_return = np.sum(weights * annual_returns)

    # Calculate Expected Volatility (sqrt(w^T * Σ * w))
    # This is the 'sigma' you will use in Black-Scholes later
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(annual_cov_matrix, weights)))

    # Financial Metric: Sharpe Ratio
    sharpe_ratio = (port_return - risk_free_rate) / port_volatility
    
    return port_return, port_volatility, sharpe_ratio

def run_sim_calc(sim_runs, n, initial_investment):
    weights_runs = np.zeros((sim_runs, n))
    sharpe_ratio_runs = np.zeros(sim_runs)
    expected_portfolio_returns_runs = np.zeros(sim_runs)
    volatility_runs = np.zeros(sim_runs)
    return_on_investment_runs = np.zeros(sim_runs)
    final_value_runs = np.zeros(sim_runs)
    
    for i in range(sim_runs):
        # Generate random weights
        weights = generate_portfolio_weights(n)
        # Store the weights
        weights_runs[i, :] = weights
    
        # Call "simulation_engine" function and store Sharpe ratio, return and volatility
        # Note that asset allocation is performed using the "asset_allocation" function
        expected_portfolio_returns_runs[i], volatility_runs[i], sharpe_ratio_runs[i], final_value_runs[i], \
        return_on_investment_runs[i] = p_sim.simulation_engine(close_price_df, weights, initial_investment)
    
        if i % 250 == 0:
            print(f"Simulation Run = {i}")
            print(f"Weights = {weights_runs[i].round(3)},"
            f"Final Value = ${final_value_runs[i]:.2f}, "
            f"Sharpe Ratio = {sharpe_ratio_runs[i]:.5f}")
            print('\n')