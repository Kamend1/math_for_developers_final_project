def calculate_optimal_weights(target_return, inv_cov, mu, ones, A, B, C, D):
    """
    Calculates the exact analytical weights for a given target return 
    allowing for short selling (unconstrained weights).
    """
    # Calculate Lagrange multipliers
    lambda_val = 2 * (A * target_return - B) / D
    gamma_val = 2 * (C - B * target_return) / D

    # Calculate optimal weights: w = (λ/2)Σ⁻¹μ + (γ/2)Σ⁻¹1
    w = (lambda_val / 2) * (inv_cov @ mu) + (gamma_val / 2) * (inv_cov @ ones)

    return w


def calculate_optimal_weights_for_range(target_returns, inv_cov, mu, ones, A, B, C, D):
    """
    Calculates the exact analytical weights for a given range of target returns 
    allowing for short selling (unconstrained weights).
    """

    frontier_weights = []

    for target_return in target_returns:
        lambda_val = 2 * (A * target_return - B) / D
        gamma_val = 2 * (C - B * target_return) / D

        w = (lambda_val / 2) * (inv_cov @ mu) + (gamma_val / 2) * (inv_cov @ ones)

        frontier_weights.append(w)

    return frontier_weights


def calculate_efficient_frontier_variance(target_returns, A, B, C, D):
    """
    Computes the closed-form variance for an array of target returns:
    σ²(μ_p) = (Aμ_p² - 2Bμ_p + C) / D
    """
    return (A * target_returns**2 - 2 * B * target_returns + C) / D