# Mathematical Foundations of Portfolio Optimization and Hedging

## 1. Project Overview & Objective

This project bridges Modern Portfolio Theory (Harry Markowitz) with Options Pricing (Black-Scholes) to construct and mathematically hedge an optimal asset portfolio. It transitions from a computational, brute-force simulation baseline to a rigorous mathematical proof utilizing matrix algebra and multivariable calculus, concluding with a stochastic calculus application to price a protective put option for the identified optimal portfolio.

## 2. Mathematical Scope

This repository specifically addresses the following mathematical requirements:

* **Linear Algebra:** Implements matrix inversion and vector dot products (Notebook 1_2) to compute the closed-form algebraic solution for the unconstrained efficient frontier ($\Sigma^{-1}$).
* **Calculus:** Utilizes gradient descent and constrained optimization (`scipy.optimize`) to locate the global minimum variance (Notebook 1_3), and applies partial derivatives to evaluate the Greeks in the Options Pricing model (Notebook 2_1).
* **Statistics & Probabilities:** Employs Monte Carlo simulations to visualize the feasible set of portfolios (Notebook 1_1) and applies the cumulative standard normal distribution function ($N(x)$) within the Black-Scholes formula (Notebook 2_1).
* **Combinatorics:** Evaluates the Efficient Frontier across discrete subsets of the selected assets to determine the optimal combinatorial portfolio structure. *(Note: Implementation location to be finalized)*

## 3. Repository Architecture

```text
├── data/                               # Auto-generated historical data and returns (CSVs)
├── project_notebooks/
│   ├── markowitz_efficient_frontier/
│   │   ├── 1_1_markowitz_efficient_frontier_practical_approach.ipynb
│   │   ├── 1_2_markowitz_efficient_frontier_mathematical_approach.ipynb
│   │   └── 1_3_markowitz_efficient_frontier_algorithmic_approach.ipynb
│   └── black_scholes_option_pricing_model/
│       └── 2_1_black_scholes_portfolio_protection.ipynb
├── src/                                # Python utility modules
│   ├── data_pipeline_utils/            # Data fetching and handling logic
│   └── portfolio_simulation_utils/     # Simulation engine and math operations
├── Final-Exam-Project-Guidelines.docx  # Academic rubric and project requirements
├── LICENSE                             # MIT License
├── README.md                           # Project documentation
└── requirements.txt                    # Environment dependencies
```

## 4. Execution Sequence

To replicate the mathematical progression and ensure data availability, the notebooks must be executed sequentially.

> **Critical Operational Note:** Notebook 1_1 handles the `yfinance` data pipeline. It must be executed first at the start of each new trading day to update the data, or whenever modifying the selected stock tickers. 
> 
> **Tip for Testing:** If you are changing tickers and only need to refresh the data in the `data/` folder, lower the `sim_runs` variable in 1_1 to 100. This accelerates the simulation block while successfully downloading the necessary CSVs for the subsequent notebooks.

**Execution Order:**

1. **`1_1_markowitz_efficient_frontier_practical_approach.ipynb`:** Fetches market data, calculates daily returns/covariance, and establishes the empirical baseline via Monte Carlo simulation.
2. **`1_2_markowitz_efficient_frontier_mathematical_approach.ipynb`:** Replaces simulation with a closed-form analytical solution (Linear Algebra) for an unconstrained portfolio (allowing short selling).
3. **`1_3_markowitz_efficient_frontier_algorithmic_approach.ipynb`:** Applies numerical optimization (Calculus) to solve the realistic, constrained portfolio (long-only), outputting the exact Tangency Portfolio weights and variance.
4. **`2_1_black_scholes_portfolio_protection.ipynb`:** Ingests the output variables from 1_3 to compute the cost of a protective put option for the exact optimal portfolio.

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