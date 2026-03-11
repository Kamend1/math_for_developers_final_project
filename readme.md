# Mathematical Foundations of Portfolio Optimization and Hedging

## 1. Project Overview & Objective

Financial risk is fundamentally a nonlinear concept. While linear approximations such as expected return or bond durations provide an idea at a certain point of these nonlinear functions, the true behavior of financial systems is driven by second-order structures such as variance, covariance, convexity, and option gamma.

This project will attempt to demonstrate how these nonlinear effects emerge in three different settings and demonstrate how solid finance theory and mathematics merge together to find practical applications in:

- Portfolio optimization
- Option pricing
- Fixed income instruments with embedded options

The project bridges Modern Portfolio Theory (Harry Markowitz) with Options Pricing (Black-Scholes) to construct and mathematically hedge an optimal asset portfolio. It transitions from a computational, brute-force simulation baseline to a rigorous mathematical proof utilizing matrix algebra and multivariable calculus, concluding with a calculus applications to price a protective put option and analyze convexity effects in financial instruments. The project also displays how optionality change the behavior of vanilla bonds by analizing a theoretical bond and a similar bond, which is callable at par.

## 2. Mathematical Scope

This repository specifically addresses the following mathematical requirements:

* **Linear Algebra:** Implements matrix inversion and vector dot products (Notebook 1_2) to compute the closed-form algebraic solution for the unconstrained efficient frontier ($\Sigma^{-1}$).
* **Calculus:** Utilizes gradient descent and constrained optimization (`scipy.optimize`) to locate the global minimum variance (Notebook 1_3), applies partial derivatives to evaluate the Greeks in the Options Pricing model (Notebook 2_1), and demonstrates Taylor approximations and convexity effects in bond pricing (Notebook 2_2).
* **Statistics & Probabilities:** Employs Monte Carlo simulations to visualize the feasible set of portfolios (Notebook 1_1) and applies the cumulative standard normal distribution function ($N(x)$) within the Black-Scholes formula (Notebook 2_1).
* **Combinatorics:** Evaluates the Efficient Frontier across discrete subsets of the selected assets to determine the optimal combinatorial portfolio structure. *(Notebook 1_3)*

## 3. Repository Architecture

```text
├── data/                               # Auto-generated historical data and returns (CSVs)
├── project_notebooks/
│   ├── markowitz_efficient_frontier/
│   │   ├── 1_1_markowitz_efficient_frontier_practical_approach.ipynb
│   │   ├── 1_2_markowitz_efficient_frontier_mathematical_approach.ipynb
│   │   └── 1_3_markowitz_efficient_frontier_algorithmic_approach.ipynb
│   └── black_scholes_option_pricing_model/
│       ├── 2_1_black_scholes_portfolio_protection.ipynb
│       └── 2_2_option_pricing_convexity_and_taylor_approximation.ipynb
├── src/                                # Python utility modules
│   ├── data_pipeline_utils/            # Data fetching and handling logic
│   ├── plotting_utils/                 # Visualization utilities
│   ├── portfolio_simulation_utils/     # Simulation engine and portfolio math
│   └── bond_calculation_utils/         # Bond pricing and convexity calculations
├── Final-Exam-Project-Guidelines.docx  # Academic rubric and project requirements
├── LICENSE                             # MIT License
├── README.md                           # Project documentation
└── requirements.txt                    # Environment dependencies
```

## 4. Execution Sequence

To replicate the mathematical progression and ensure data availability, the notebooks must be executed sequentially especially for books 1_1, 1_2, 1_3 and 2_1.

> **Critical Operational Note:** Notebook 1_1 handles the `yfinance` data pipeline. It must be executed first at the start of each new trading day to update the data, or whenever modifying the selected stock tickers. 
> 
> **Tip for Testing:** If you are changing tickers and only need to refresh the data in the `data/` folder, lower the `sim_runs` variable in 1_1 to a small number like 100. This accelerates the simulation block while successfully downloading the necessary CSVs for the subsequent notebooks.

**Execution Order:**

1. **`1_1_markowitz_efficient_frontier_practical_approach.ipynb`:** Fetches market data, calculates daily returns/covariance, and establishes the empirical baseline via Monte Carlo simulation.
2. **`1_2_markowitz_efficient_frontier_mathematical_approach.ipynb`:** Replaces simulation with a closed-form analytical solution (Linear Algebra) for an unconstrained portfolio (allowing short selling).
3. **`1_3_markowitz_efficient_frontier_algorithmic_approach.ipynb`:** Applies numerical optimization (Calculus) to solve the realistic, constrained portfolio (long-only), outputting the exact Tangency Portfolio weights and variance.
4. **`2_1_black_scholes_portfolio_protection.ipynb`:** Ingests the output variables from 1_3 to compute the cost of a protective put option for the exact optimal portfolio
and finally 
5. **`2_2_option_pricing_in_bonds.ipynb`:** which illustrates bond behavior with options and is not related to the other notebooks.

## 5. Installation and Setup

Ensure you have Python 3.9+ installed. Clone the repository and install the required scientific libraries:

```bash
git clone <your-repository-url>
cd <repository-name>
pip install -r requirements.txt
```

Launch Jupyter to begin execution:

```bash
jupyter notebook
```

## Note on Development Tools

During the development of this project I used a variety of standard software tools and learning resources, including Python documentation, academic literature (CFA Institute materials, Frank Fabozzi, John Hull, etc.), and AI-assisted coding and writing tools.

These tools were used primarily for:
- improving code structure,
- verifying mathematical expressions,
- refining and polishing written explanations.
- fixing constant challenges with LaTeX as I went through a learning curve with it

All mathematical modeling, implementation decisions, and interpretation of results were developed and verified by the author.

## Note to the Lecturer

Dear Yordan,

During the course you mentioned that portfolio optimization and Monte Carlo simulations are themes you have encountered way too many times in student projects. That comment stayed with me while developing this work.

Coming from over twenty years of experience in finance, I initially assumed that combining practical portfolio construction with the mathematical tools explored in this course would still provide an interesting perspective — especially when extended toward option pricing, curvature analysis, and the geometric interpretation of financial payoffs.

My goal with this project was therefore not simply to reproduce known models, but to connect several ideas together: portfolio optimization, derivatives, Taylor approximations, and the role of curvature in financial decision-making.

I hope the result offers a slightly different angle on a familiar topic — one coming from the intersection of industry practice and newly developed mathematical intuition.

As a proud alumnus of the Python Web Development track, I also aimed to structure the notebooks clearly and keep the computational parts efficient and reproducible.

Thank you for the course and for pushing us to look at these topics from a deeper mathematical perspective.