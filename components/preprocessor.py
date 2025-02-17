import pandas as pd
from .utils.qa_functions import (
    check_missing_values,
    check_duplicates,
    check_data_types,
    check_value_ranges,
    clean_extra_strs,
    check_unique_values,
    check_date_format,
    print_separator,
    decompose_dates
)
from .utils.feature_functions import create_extra_features

class Preprocessor:
    def __init__(self, date_col: str = "date", value_date_col: str = "value_date", model_features_path: str = "model_features.csv") -> None:
        """
        Initializes the Preprocessor component.

        Args:
            date_col (str): The name of the date column.
            value_date_col (str): The name of the value date column.
        """
        print("====================================")
        print("Starting Preprocessor Component")
        print("====================================\n")
        self.date_col = date_col
        self.value_date_col = value_date_col
        self.features = pd.read_csv(model_features_path)

        print("- Expected raw model features:\n", self.features, "\n")
        print("- Date col:", self.date_col)
        print("- Value date col:", self.value_date_col)


    def check_columns_exist(self, X: pd.DataFrame, columns: list) -> None:
        """
        Checks if the raw features that the model saw during training exist in the input DataFrame.
        Raises an exception if any of the expected features are missing.

        Args:
            X (pd.DataFrame): The input DataFrame.
            columns (list): The list of columns to check.

        Raises:
            ValueError: If any of the specified columns are missing.
        """
        missing_columns = [col for col in columns if col not in X.columns]
        if missing_columns:
            raise ValueError(f"Missing expected raw features in input DataFrame: {', '.join(missing_columns)}")
        
    def run_quality_checks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes all data quality checks.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame after performing quality checks.
        """
        # Null check and cleaning
        check_missing_values(df)
        
        print("Rows before cleaning nulls:", df.shape[0], "Columns:", df.shape[1])
        df.drop(columns=["chq_no"], inplace=True)
        df = df[~df.transaction_details.isnull()]
        print("Rows after cleaning nulls:", df.shape[0], "Columns:", df.shape[1])
        print_separator()
        
        # Duplicates
        df = check_duplicates(df)
        print_separator()
        
        # Data types
        df = check_data_types(df)
        print_separator()
        
        # Value ranges
        df = check_value_ranges(df)
        
        # Clean extra characters
        df = clean_extra_strs(df)
        print_separator()

        # Unique values per category
        df = check_unique_values(df)

        # Date format check
        date_columns = [col for col in df.columns if "date" in col]
        df = check_date_format(df, date_columns)
        print_separator()

        # Final DataFrame
        print("===== Dataframe post cleaning =====")
        print(df)
        return df
    
    def preprocess(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the input DataFrame by running quality checks and decomposing dates.

        Args:
            X (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The preprocessed DataFrame.
        """
        self.check_columns_exist(X, self.features)
        X = self.run_quality_checks(X)
        X = create_extra_features(X)
        X = decompose_dates(X, date_col=self.date_col, value_date_col=self.value_date_col)
        return X