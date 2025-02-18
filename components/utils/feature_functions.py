import pandas as pd
import numpy as np
from typing import Optional

def classify_transactions(
    X: pd.DataFrame, 
    withdrawal_col: str = 'withdrawal_amt', 
    deposit_col: str = 'deposit_amt', 
    transaction_type_col: str = 'transactionType'
) -> pd.DataFrame:
    """
    Classify transactions in the given DataFrame.

    Parameters:
        X (pd.DataFrame): The input DataFrame.
        withdrawal_col (str): The name of the withdrawal amount column. Default is 'withdrawal_amt'.
        deposit_col (str): The name of the deposit amount column. Default is 'deposit_amt'.
        transaction_type_col (str): The name of the transaction type column to be created. Default is 'transactionType'.

    Returns:
        pd.DataFrame: The DataFrame with the transaction type column added.
    """
    X[transaction_type_col] = np.where(
        (X[withdrawal_col] > 0) & pd.isnull(X[deposit_col]), 'withdrawal', 
        np.where(pd.isnull(X[withdrawal_col]) & (X[deposit_col] > 0), 'deposit',
        np.where(pd.isnull(X[withdrawal_col]) & pd.isnull(X[deposit_col]), 'no transaction', 'both')
        )
    )
    return X

def calculate_date_diff(
    X: pd.DataFrame, 
    value_date_col: str = 'value_date', 
    date_col: str = 'date', 
    date_diff_col: str = 'date_diff'
) -> pd.DataFrame:
    """
    Calculate the difference between value date and date in the given DataFrame.

    Parameters:
        X (pd.DataFrame): The input DataFrame.
        value_date_col (str): The name of the value date column. Default is 'value_date'.
        date_col (str): The name of the date column. Default is 'date'.
        date_diff_col (str): The name of the date difference column to be created. Default is 'date_diff'.

    Returns:
        pd.DataFrame: The DataFrame with the date difference column added.
    """
    X[date_diff_col] = (X[value_date_col] - X[date_col]).dt.days
    return X

def compress_low_frequency_categories(
    X: pd.DataFrame, 
    category_col: str = 'category', 
    target_category_col: str = 'target_category'
) -> pd.DataFrame:
    """
    Compress low frequency categories in the given DataFrame.

    Parameters:
        X (pd.DataFrame): The input DataFrame.
        category_col (str): The name of the category column. Default is 'category'.
        target_category_col (str): The name of the target category column to be created. Default is 'target_category'.

    Returns:
        pd.DataFrame: The DataFrame with the compressed categories.
    """
    classes = X[category_col].value_counts().index.tolist()
    
    # TODO move this to a config file
    low_freq = ['Pets & Pet Care', 'Travel',
       'Insurance', 'Transportation', 'Health & Wellness', 'Entertainment',
       'Education', 'Childcare & Parenting']
    not_low_freq = [x for x in classes if x not in low_freq]
    X[target_category_col] = X[category_col].apply(lambda x: 'others' if x not in not_low_freq else x)
    X.drop(category_col, axis=1, inplace=True)
    
    return X

def create_extra_features(
    X: pd.DataFrame, 
    withdrawal_col: str = 'withdrawal_amt', 
    deposit_col: str = 'deposit_amt', 
    transaction_type_col: str = 'transactionType', 
    value_date_col: str = 'value_date', 
    date_col: str = 'date', 
    date_diff_col: str = 'date_diff', 
    category_col: str = 'category', 
    target_category_col: str = 'target_category'
) -> pd.DataFrame:
    """
    Create extra features for the given DataFrame by combining the functionalities of the other functions.

    Parameters:
        X (pd.DataFrame): The input DataFrame.
        withdrawal_col (str): The name of the withdrawal amount column. Default is 'withdrawal_amt'.
        deposit_col (str): The name of the deposit amount column. Default is 'deposit_amt'.
        transaction_type_col (str): The name of the transaction type column to be created. Default is 'transactionType'.
        value_date_col (str): The name of the value date column. Default is 'value_date'.
        date_col (str): The name of the date column. Default is 'date'.
        date_diff_col (str): The name of the date difference column to be created. Default is 'date_diff'.
        category_col (str): The name of the category column. Default is 'category'.
        target_category_col (str): The name of the target category column to be created. Default is 'target_category'.

    Returns:
        pd.DataFrame: The DataFrame with the new features added.
    """
    X = classify_transactions(X, withdrawal_col, deposit_col, transaction_type_col)
    X = calculate_date_diff(X, value_date_col, date_col, date_diff_col)
    X = compress_low_frequency_categories(X, category_col, target_category_col)
    
    return X