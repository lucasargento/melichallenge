'''
This file simulates batch data loading from BigQuery (or any other warehouse) for 
demonstration purposes. The data is loaded from a parquet file and returned as a 
data frame in this file.
'''
import pandas as pd
import os
from datetime import datetime

class BatchFetcher:
    def __init__(
            self, 
            mode: str = "inference",
            file_path: str = "bank_transactions.parquet", 
            out_sample_path: str = "bank_transactions_outsample.parquet",
        ):
        """
        Initialize the BatchFetcher with the path to the parquet file.

        params
            file_path: Path to the parquet file.
        """
        if mode == "inference":
            self.file_path = out_sample_path
        else:
            self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the parquet file.

        returns:
            DataFrame containing the loaded data, or None if an error occurs.
        """
        try:
            cwd = os.getcwd()
            data = pd.read_parquet(f"{cwd}/data/{self.file_path}")
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def write_to_bq(self, df: pd.DataFrame, table_name: str):
        """
        Write data to a BigQuery table. (simulated: it will instead write into a csv at /outputs dir)

        params
            df: DataFrame containing the data to write.
            table_name: Name of the table to write to.
        """
        try:
            # write data to BigQuery
            print(f"Writing data to BigQuery table {table_name}...")
            now = datetime.now()
            df.to_csv(f"outputs/{table_name}.csv", index=False)
        except Exception as e:
            print(f"Error writing data to BigQuery: {e}")