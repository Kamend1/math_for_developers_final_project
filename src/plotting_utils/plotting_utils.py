import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from src.data_pipeline_utils import data_fetching_handling as data_pipe

def plot_taylor_expansion(x_range, true_values, target_x, target_y, 
                           tangent_values=None, quadratic_values=None, 
                           payoff_values=None, title="Financial Sensitivity Analysis", 
                           xlabel="Input", ylabel="Price/Value", vline_x=None):
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

def create_histogram_distribution_daily_log_returns(ticker):
    data = data_pipe.fetch_returns_data(ticker)
    
    fig = plt.figure(figsize=(10,6))
    plt.hist(data["log_return_pct"], bins=100)
    plt.title(F"Distribution of {ticker} Daily Log Returns")
    plt.xlabel("Log Return")
    plt.ylabel("Frequency")
    return fig


def create_correlation_heatmap(corr_matrix):
    fig = plt.figure(figsize=(8,6))
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
