'''
    File containing axuiliary functions for data quality assessment.
    Usually called in the Preprocessor component or usefull for Pre-EDA processing.
'''
import pandas as pd
from pandas import DataFrame

def check_missing_values(df: DataFrame) -> DataFrame:
    """
    Checks for missing values in each column and displays the count of nulls over the total rows.

    Args:
        df (DataFrame): The DataFrame to check for missing values.

    Returns:
        DataFrame: The original DataFrame.
    """
    totals = df.shape[0]
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    missing_percentage = (missing / totals) * 100

    missing_summary = pd.DataFrame({
        'Missing Values': missing,
        'Percentage': missing_percentage
    })
    print("Missing Values Summary")
    print(missing_summary)
    return df

def check_duplicates(df: DataFrame) -> DataFrame:
    """
    Checks for duplicate records.

    Args:
        df (DataFrame): The DataFrame to check for duplicates.

    Returns:
        DataFrame: The DataFrame with duplicates removed if any were found.
    """
    duplicates = df.duplicated().sum()
    print(f"Duplicate records: {duplicates}")
    
    if duplicates > 0:
        df = df.drop_duplicates()
        print("Duplicates removed.")
    
    return df

def check_data_types(df: DataFrame) -> DataFrame:
    """
    Checks the data types and possible issues.

    Args:
        df (DataFrame): The DataFrame to check data types.

    Returns:
        DataFrame: The original DataFrame.
    """
    print("Data types:")
    print(df.dtypes)
    return df

def check_value_ranges(df: DataFrame) -> DataFrame:
    """
    Checks for out-of-range values in numeric columns.

    Args:
        df (DataFrame): The DataFrame to check value ranges.

    Returns:
        DataFrame: The original DataFrame.
    """
    summary = df.describe()
    print("Statistical summary of numeric values:")
    print(summary)
    
    for col in df.columns:
        if "date" in col:
            print(f"Date range for column {col}: {df[col].min()} || {df[col].max()}")
    
    return df

def clean_extra_strs(df: DataFrame, target_column: str = "account_id", target_str: str = "'") -> DataFrame:
    """
    Cleans extra strings from a target column.

    Args:
        df (DataFrame): The DataFrame to clean.
        target_column (str): The column to clean. Default is "account_id".
        target_str (str): The string to remove. Default is "'".

    Returns:
        DataFrame: The DataFrame with cleaned column.
    """
    df[target_column] = df[target_column].str.replace(target_str, "")
    return df

def check_unique_values(df: DataFrame) -> DataFrame:
    """
    Checks how many unique values each categorical column has.

    Args:
        df (DataFrame): The DataFrame to check unique values.

    Returns:
        DataFrame: The original DataFrame.
    """
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        unique_values = df[col].nunique()
        print(f"The column '{col}' has {unique_values} unique values.")

        if unique_values < 20:
            print("\n ==> ", df[col].unique())
        
        print("\n---------------")
    return df
    
def check_date_format(df: DataFrame, date_cols: list[str]) -> DataFrame:
    """
    Converts columns to datetime and checks for erroneous values.

    Args:
        df (DataFrame): The DataFrame to check date formats.
        date_cols (list[str]): List of columns to convert to datetime.

    Returns:
        DataFrame: The DataFrame with date columns converted.
    """
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        invalid_dates = df[df[col].isnull()]
        if invalid_dates.shape[0] > 0:
            print(f"⚠️ {invalid_dates.shape[0]} invalid values in {col}")
    return df

def print_separator() -> None:
    """
    Prints a separator line.
    """
    print("\n=====================\n")


def decompose_dates(X: pd.DataFrame, date_col: str, value_date_col: str) -> pd.DataFrame:
    """
    Decomposes date columns into separate year, month, day, and weekday columns.

    Args:
        X (pd.DataFrame): The input DataFrame containing date columns.

    Returns:
        pd.DataFrame: The DataFrame with decomposed date columns.
    """

    # Decompose the dates
    X['year'] = X[date_col].dt.year
    X['month_date'] = X[date_col].dt.month
    X['day'] = X[date_col].dt.day
    X['weekday'] = X[date_col].dt.weekday

    X['year_value_date'] = X[value_date_col].dt.year
    X['month_value_date'] = X[value_date_col].dt.month
    X['day_value_date'] = X[value_date_col].dt.day
    X['weekday_value_date'] = X[value_date_col].dt.weekday
    X['month'] = X[date_col].dt.month

    # Drop the original date columns after extracting the features
    X = X.drop(columns=[date_col, value_date_col])
    
    return X