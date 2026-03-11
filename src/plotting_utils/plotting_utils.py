import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from src.data_pipeline_utils import data_fetching_handling as data_pipe


def plot_taylor_expansion(x_range,
                          true_values,
                          target_x,
                          target_y,
                          title="Financial Sensitivity Analysis",
                          xlabel="Input",
                          ylabel="Price/Value",
                          tangent_values=None,
                          quadratic_values=None,
                          payoff_values=None,
                          vline_x=None):
    """
    A unified method to plot Price Functions, Tangents (1st Order), 
    and Convexity (2nd Order).
    """
    fig = plt.figure(figsize=(10, 6))

    # 1. Plot the price function
    plt.plot(x_range, true_values, color='navy', lw=3, label='Actual Price (Ground Truth)')

    # 2. Plot First Order Approximation (Tangent/Linear/Duration/Delta)
    if tangent_values is not None:
        plt.plot(x_range, tangent_values, '--', color='orange', label='1st Order (Linear/Tangent)')

    # 3. Plot Second Order Approximation (Quadratic/Convexity/Gamma)
    if quadratic_values is not None:
        plt.plot(x_range, quadratic_values, ':', color='dodgerblue', lw=2.5, label='2nd Order (Quadratic/Convex)')

    # 4. Plot Payoff (Specific to Options)
    if payoff_values is not None:
        plt.plot(x_range, payoff_values, linestyle=':', color='black', alpha=0.6, label='Payoff at Expiry')

    # 5. Mark the Analysis Point
    plt.scatter([target_x], [target_y], color='red', zorder=5, label=f'Target Point ({target_y:.2f})')

    # 6. Add Vertical Reference (Strike or Target Yield)
    if vline_x is not None:
        plt.axvline(vline_x, color='red', linestyle='--', alpha=0.5, label='Threshold/Strike')

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(alpha=0.3)

    return fig


def create_candlestick_graph(ticker):
    """
    Constructs a daily OHLC candlestick visualization for a given financial ticker.

    The function utilizes 'data_pipe.fetch_raw_data' to acquire historical time-series 
    data and encapsulates it into a Plotly Figure object. The layout is standardized 
    to prioritize price-scale clarity by disabling the default range slider.

    Args:
        ticker: The ticker symbol (e.g., 'AAPL', 'MSFT') to be retrieved and plotted.

    Returns:
        plotly.graph_objects.Figure: A configured Plotly figure object ready for 
            interactive rendering.

    Notes:
        Requires the 'data_pipe' module to be initialized and accessible within 
        the function's scope.
    """

    data = data_pipe.fetch_raw_data(ticker)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=f"{ticker}"
            )
        ]
    )

    fig.update_layout(
        title=F"{ticker} Daily Candlestick",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    return fig


def create_histogram_distribution_daily_log_returns(return_data, ticker, mean=None, st_dev=None):
    """
    Generates a frequency distribution of daily log returns with statistical overlays.

    This function plots an empirical histogram of the returns and annotates the 
    distribution with the arithmetic mean and standard deviation boundaries (1σ and 2σ). 
    It is designed to visualize volatility clustering and the 'fat-tailed' nature 
    (kurtosis) of financial time-series data.

    Args:
        return_data (pd.DataFrame): DataFrame containing a 'log_return_pct' column.
        ticker (str): The financial instrument symbol for labeling purposes.
        mean (float, optional): The population or sample mean of the log returns.
        st_dev (float, optional): The standard deviation (volatility) of the log returns.

    Returns:
        matplotlib.figure.Figure: The figure object containing the histogram and 
            statistical markers.

    Note:
        The function assumes standard deviation and mean parameters are provided in 
        decimal form (e.g., 0.02 for 2%) and automatically scales them to match the 
        percentage-based data in the histogram.
    """

    if mean is not None:
        mean_pct = mean * 100

    if st_dev is not None:
        st_dev_pct = st_dev * 100

    fig = plt.figure(figsize=(10, 6))
    plt.hist(return_data["log_return_pct"], bins=100, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(mean, label='Mean', color='r')

    if mean is not None and st_dev is not None:
        plt.axvline(mean_pct - st_dev_pct, label='+/- 1 St Dev', color='y', linestyle='dashed')
        plt.axvline(mean_pct + st_dev_pct, label='+/- 1 St Dev', color='y', linestyle='dashed')
        plt.axvline(mean_pct - 2*st_dev_pct, label='+/- 2 St Dev', color='orange', linestyle='dashed')
        plt.axvline(mean_pct + 2*st_dev_pct, label='+/- 2 St Dev', color='orange', linestyle='dashed')

    plt.title(F"Distribution of {ticker} Daily Log Returns", fontsize=14)
    plt.xlabel("Log Return", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.legend()
    return fig


def create_histogram_distribution_portfolio_metrics(metric,
                                                    title="Distribution of Variations",
                                                    xlabel=" Metric Deviation (Spread)",
                                                    ylabel='Frequency (Number of Portfolio Combinations)'):
    """
    Generates a frequency distribution of a given metric with statistical overlays.
    """

    plt.figure(figsize=(10, 6))
    plt.hist(metric, bins=10, color='skyblue', edgecolor='black', alpha=0.7)

    plt.axvline(np.mean(metric),
                color='red',
                linestyle='dashed',
                linewidth=2,
                label=f'Mean: {np.mean(metric):.4f}')

    plt.axvline(np.median(metric),
                color='green',
                linestyle='dashed',
                linewidth=2,
                label=f'Median: {np.median(metric):.4f}')

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()


def create_correlation_heatmap(corr_matrix):
    """
    Generates an annotated heatmap to visualize linear relationships between assets.

    This matrix is essential for identifying diversification potential; values closer 
    to 1 indicate high redundancy, while values near 0 or -1 suggest hedging benefits.

    Args:
        corr_matrix (pd.DataFrame): A square matrix of correlation coefficients (r), 
            ideally within the range of [-1, 1].

    Returns:
        matplotlib.figure.Figure: The figure object containing the 'coolwarm' 
            centered heatmap.
    """

    fig = plt.figure(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.5
    )

    plt.title("Correlation Matrix Heatmap")
    return fig


def create_sim_output_scatter(cloud_df, optimal_portfolio):
    """
    Visualizes the risk-return simulation 'cloud' and highlights the tangency portfolio.

    Args:
        cloud_df (pd.DataFrame): Simulated portfolios with Volatility, Portfolio_Return, and Sharpe_Ratio.
        optimal_portfolio (dict/pd.Series): Coordinates for the portfolio maximizing the Sharpe Ratio.

    Returns:
        plotly.graph_objects.Figure: Interactive scatter plot with the 'Optimal' marker overlaid.
    """

    fig = px.scatter(
        cloud_df,
        x="Volatility",
        y="Portfolio_Return",
        color="Sharpe_Ratio",
        size="Sharpe_Ratio",
        opacity=0.5,
        hover_data=["Sharpe_Ratio"]
    )

    fig.add_trace(go.Scatter(
        x=[optimal_portfolio["Volatility"]],
        y=[optimal_portfolio["Portfolio_Return"]],
        mode="markers+text",
        marker=dict(color="red", size=25, line=dict(color="orange", width=2)),
        name="Optimal Portfolio",
        text=["Optimal"],
        textposition="top left"
    ))

    fig.update_layout(plot_bgcolor="white")
    return fig


def sim_results_plot(sim_out_df):
    """
    Generates a trio of interactive line plots to track portfolio metrics across simulations.

    Args:
        sim_out_df (pd.DataFrame): Simulation output containing 'Volatility', 
            'Portfolio_Return', and 'Sharpe_Ratio' columns.

    Returns:
        tuple: Three Plotly Figure objects representing Volatility, Return, and Sharpe Ratio trends.
    """

    # Plot interactive plot for volatility
    fig_1 = px.line(sim_out_df, y='Volatility')

    # Plot interactive plot for Portfolio Return
    fig_2 = px.line(sim_out_df, y='Portfolio_Return')
    fig_2.update_traces(line_color='red')

    # Plot interactive plot for Portfolio Return
    fig_3 = px.line(sim_out_df, y='Sharpe_Ratio')
    fig_3.update_traces(line_color='purple')

    return fig_1, fig_2, fig_3


def plot_3d_portfolio_surface(w1_grid, w2_grid, risk_grid):
    """
    Renders the 'Risk Bowl' surface for a two-asset universe.
    
    This visualization illustrates the quadratic nature of portfolio variance. 
    The lowest point on the surface represents the Global Minimum Variance (GMV) 
    position before applying the budget constraint (w1 + w2 = 1).

    Args:
        w1_grid (np.ndarray): 2D meshgrid of weights for the first asset.
        w2_grid (np.ndarray): 2D meshgrid of weights for the second asset.
        risk_grid (np.ndarray): 2D meshgrid of calculated portfolio standard deviations.

    Returns:
        go.Figure: A Plotly figure with adjusted aspect ratios for topographical clarity.
    """
    fig = go.Figure(data=[go.Surface(
        z=risk_grid, 
        x=w1_grid, 
        y=w2_grid, 
        lighting=dict(ambient=0.6, diffuse=0.5, roughness=0.9)
    )])

    fig.update_layout(
        title='Portfolio Risk Topology',
        autosize=True,
        width=1000,
        height=800,
        scene=dict(
            aspectmode='cube',
            xaxis_title='w₁ (Asset A)',
            yaxis_title='w₂ (Asset B)',
            zaxis_title='Standard Deviation (σ)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=0.8)
            )
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig