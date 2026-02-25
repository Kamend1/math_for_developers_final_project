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

def price_scaling(raw_prices_df):
    return raw_prices_df / raw_prices_df.iloc[0]

def asset_allocation(df, weights, initial_investment):
    portfolio_df = df.copy()

    # Scale stock prices using the "price_scaling" function that we defined earlier (Make them all start at 1)
    scaled_df = price_scaling(df)

    for i, stock in enumerate(scaled_df.columns[1:]):
        portfolio_df[stock] = scaled_df[stock] * weights[i] * initial_investment

    # Sum up all values and place the result in a new column titled "portfolio value [$]"
    # Note that we excluded the date column from this calculation
    portfolio_df['Portfolio Value [$]'] = portfolio_df[portfolio_df != 'Date'].sum(axis=1, numeric_only=True)

    # Calculate the portfolio percentage daily return and replace NaNs with zeros
    portfolio_df['Portfolio Daily Return [%]'] = portfolio_df['Portfolio Value [$]'].pct_change(1) * 100
    portfolio_df.replace(np.nan, 0, inplace=True)

    return portfolio_df

def simulation_engine(close_price_df, weights, initial_investment):
    # Perform asset allocation using the random weights (sent as arguments to the function)
    portfolio_df = asset_allocation(close_price_df, weights, initial_investment)

    # Calculate the return on the investment
    # Return on investment is calculated using the last final value of the portfolio compared to its initial value
    return_on_investment = ((portfolio_df['Portfolio Value [$]'].iloc[-1] -
                             portfolio_df['Portfolio Value [$]'].iloc[0]) /
                            portfolio_df['Portfolio Value [$]'].iloc[0]) * 100

    # Daily change of every stock in the portfolio (Note that we dropped the date, portfolio daily worth and daily % returns)
    portfolio_daily_return_df = portfolio_df.drop(columns=['Portfolio Value [$]', 'Portfolio Daily Return [%]'])
    portfolio_daily_return_df = portfolio_daily_return_df.pct_change(1)

    # Portfolio Expected Return formula
    expected_portfolio_return = np.sum(weights * portfolio_daily_return_df.mean()) * 252

    # Portfolio volatility (risk) formula
    # The risk of an asset is measured using the standard deviation which indicates the dispertion away from the mean
    # The risk of a portfolio is not a simple sum of the risks of the individual assets within the portfolio
    # Portfolio risk must consider correlations between assets within the portfolio which is indicated by the covariance
    # The covariance determines the relationship between the movements of two random variables
    # When two stocks move together, they have a positive covariance when they move inversely, the have a negative covariance

    covariance = portfolio_daily_return_df.cov() * 252
    expected_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance, weights)))

    # Check out the chart for the 10-years U.S. treasury at https://ycharts.com/indicators/10_year_treasury_rate
    rf = 0.03  # Try to set the risk free rate of return to 1% (assumption)

    # Calculate Sharpe ratio
    sharpe_ratio = (expected_portfolio_return - rf) / expected_volatility
    return expected_portfolio_return, expected_volatility, sharpe_ratio, \
    portfolio_df['Portfolio Value [$]'].iloc[-1], return_on_investment

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