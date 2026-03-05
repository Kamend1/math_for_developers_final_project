import matplotlib.pyplot as plt
import numpy as np

def plot_taylor_expansion(x_range, true_values, target_x, target_y, 
                           tangent_values=None, quadratic_values=None, 
                           payoff_values=None, title="Financial Sensitivity Analysis", 
                           xlabel="Input", ylabel="Price/Value", vline_x=None):
    """
    A unified method to plot Price Functions, Tangents (1st Order), 
    and Convexity (2nd Order).
    """
    plt.figure(figsize=(10, 6))
    
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
    plt.show()