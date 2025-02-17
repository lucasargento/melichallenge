import pandas as pd
import pickle
from typing import Any, Union
import os

class ClassificationPipeline:
    def __init__(self, weights_path: str = "latest", mode: str = "inference"):
        """
        Initialize the ClassificationPipeline.

        Parameters:
            weights_path (str): Path to a SPECIFIC model weights file. if not specified, 
                it will default to the latest version
            mode (str): Mode of operation, either 'inference' or other. Default is 'inference'.
        """
        print("\n====================================")
        print("Starting Classifier Pipeline Component")
        print("====================================\n")
        self.weights_path = weights_path
        self.mode = mode
        if self.mode == "inference":
            self.model = self.load_model()

        print("- Weights at:", self.weights_path)
        print("- Mode:", self.mode)

    def load_model(self) -> Union[Any, None]:
        """
        Load the model from the specified weights path.

        Returns:
            model (Any): The loaded model object, or None if loading fails.
        """
        try:
            print("Current working directory:", os.getcwd())
            cwd = os.getcwd()
            
            # simulate getting latest versions from "model registry"
            files = os.listdir(f"{cwd}/weights")
            files = [file for file in files if ".pkl" in file]
            
            suffixes = [f.split('_v')[-1] for f in files]
            suffixes = [s.split('.')[0] for s in suffixes]

            print("Model versions in weights directory:", suffixes)
            latest_version = max([int(s) for s in suffixes])

            if self.weights_path != "latest":
                model = pickle.load(open(f"{cwd}/weights/{self.weights_path}", 'rb'))
            else:
                model = pickle.load(open(f"{cwd}/weights/trained_pipeline_v{latest_version}.pkl", 'rb'))

            return model
        except Exception as e:
            print("Error loading model:", e)
            return None
    
    def run_realtime_pred(self, X: pd.DataFrame) -> Any:
        """
        Perform real-time prediction on the input data.

        Parameters:
            X (pd.DataFrame): Input data for prediction.

        Returns:
            Any: Prediction results or an error message if not in inference mode.
        """
        if self.mode == "inference":
            return self.model.predict(X)
        else:
            return "Can't perform realtime inference if not in inference mode."

    def run_batch_pred(self, X: pd.DataFrame) -> Union[pd.DataFrame, str]:
        """
        Perform batch prediction on the input data.

        Parameters:
            X (pd.DataFrame): Input data for prediction.

        Returns:
            pd.DataFrame: Prediction results or an error message if not in inference mode.
        """
        if self.mode == "inference":
            return self.model.predict(X)
        else:
            return "Can't perform batch inference if not in inference mode."