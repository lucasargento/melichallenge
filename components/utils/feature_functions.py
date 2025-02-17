import pandas as pd
import numpy as np
from typing import Optional

def create_extra_features(
    X: pd.DataFrame, 
    withdrawal_col: str = 'withdrawal_amt', 
    deposit_col: str = 'deposit_amt', 
    transaction_type_col: str = 'transactionType', 
    value_date_col: str = 'value_date', 
    date_col: str = 'date', 
    date_diff_col: str = 'date_diff'
) -> pd.DataFrame:
    """
    Create extra features for the given DataFrame.

    Parameters:
        X (pd.DataFrame): The input DataFrame.
        withdrawal_col (str): The name of the withdrawal amount column. Default is 'withdrawal_amt'.
        deposit_col (str): The name of the deposit amount column. Default is 'deposit_amt'.
        transaction_type_col (str): The name of the transaction type column to be created. Default is 'transactionType'.
        value_date_col (str): The name of the value date column. Default is 'value_date'.
        date_col (str): The name of the date column. Default is 'date'.
        date_diff_col (str): The name of the date difference column to be created. Default is 'date_diff'.

    Returns:
        pd.DataFrame: The DataFrame with the new features added.
    """
    # Create a classification of the transaction
    X[transaction_type_col] = np.where(
        (X[withdrawal_col] > 0) & pd.isnull(X[deposit_col]), 'withdrawal', 
        np.where(pd.isnull(X[withdrawal_col]) & (X[deposit_col] > 0), 'deposit',
        np.where(pd.isnull(X[withdrawal_col]) & pd.isnull(X[deposit_col]), 'no transaction', 'both')
        )
    )
    # Calculate the difference between 'value_date' and 'date'
    X[date_diff_col] = (X[value_date_col] - X[date_col]).dt.days
    return X