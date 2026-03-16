import pandas as pd
import yfinance as yf
import numpy as np
from pathlib import Path


def save_10_year_single_stock_data_to_csv(ticker: str, per: str = "10y") -> pd.DataFrame:
    """
    Download historical data from yfinance for a ticker and a period. Period defaults to 10y
    if not provided. Save the information in a data folder in the main project folder. If data
    folder is not available, it is first created
    """
    data = yf.download(ticker,
                       period=per,
                       interval="1d",
                       auto_adjust=True,
                       progress=False)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    filename = data_dir / f"{ticker}_{per}_auto_adjusted.csv"
    data.to_csv(filename)

    return data


def create_returns_and_save(
    df: pd.DataFrame,
    ticker: str,
    period: str = "10y",
    data_folder: str = "data") -> pd.DataFrame:
    """
    Create a derived dataset containing daily arithmetic and logarithmic returns,
    save it as a new CSV file in the specified data folder, and return the new DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input price DataFrame containing at minimum a 'Close' column.
        The index is expected to be a DatetimeIndex.

    ticker : str
        Stock ticker symbol used for naming the output file.

    period : str, default="10y"
        Period label used in the output filename.

    data_folder : str, default="data"
        Directory where the resulting CSV file will be stored.
        The folder will be created if it does not exist.

    Returns
    -------
    pd.DataFrame
        A new DataFrame containing:
        - daily_return : arithmetic daily return (percentage change)
        - log_return   : logarithmic daily return

        The first row is removed due to undefined return values.

    Notes
    -----
    - Arithmetic returns are computed as:
        R_t = (P_t / P_{t-1}) - 1

    - Logarithmic returns are computed as:
        r_t = ln(P_t / P_{t-1})

    - The original DataFrame is not modified.
    - The output file is named:
        {ticker}_{period}_with_returns.csv
    """

    new_df = df.copy()

    new_df["daily_return"] = new_df["Close"].pct_change()
    new_df["log_return"] = np.log(
        new_df["Close"] / new_df["Close"].shift(1)
    )
    new_df["daily_return_pct"] = new_df["daily_return"] * 100
    new_df["log_return_pct"] = new_df["log_return"] * 100

    new_df = new_df.dropna()

    data_path = Path(data_folder)
    data_path.mkdir(exist_ok=True)

    filename = data_path / f"{ticker}_{period}_with_returns.csv"
    new_df.to_csv(filename)

    return new_df


def percentage_return_classifier(percentage_return):
    """
    Classify the daily returns in seven categories
    """
    if percentage_return > -0.3 and percentage_return <= 0.3:
        return 'Insignificant Change'
    elif percentage_return > 0.3 and percentage_return <= 3:
        return 'Positive Change'
    elif percentage_return > -3 and percentage_return <= -0.3:
        return 'Negative Change'
    elif percentage_return > 3 and percentage_return <= 7:
        return 'Large Positive Change'
    elif percentage_return > -7 and percentage_return <= -3:
        return 'Large Negative Change'
    elif percentage_return > 7:
        return 'Bull Run'
    elif percentage_return <= -7:
        return 'Bear Sell Off'


def fetch_raw_data(ticker, period="10y", data_folder="data"):
    """
    This method reads CSV files, which have been previously saved to
    data folder
    """
    
    file_path = Path(data_folder) / f"{ticker}_{period}_auto_adjusted.csv"
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)

    return data


def build_close_price_df(tickers, period="10y", data_folder="data"):
    """
    Extract close prices by ticker in a new DataFrame object
    """
    close_price_df = pd.DataFrame()

    for ticker in tickers:
        df = fetch_raw_data(ticker)
        close_price_df[ticker] = df["Close"]

    return close_price_df


def fetch_returns_data(ticker, period="10y", data_folder="data"):
    """
    Extract return calculations by ticker in a new DataFrame object
    """
    file_path = Path(data_folder) / f"{ticker}_{period}_with_returns.csv"
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)

    return data


def build_returns_df(tickers, period="10y", data_folder="data"):
    """
    Create CSV file with return calculations by ticker and save in data folder
    """
    
    returns_df = pd.DataFrame()

    for ticker in tickers:
        return_data = fetch_returns_data(ticker)

        returns_df[ticker] = return_data["log_return"].dropna()

    return returns_df