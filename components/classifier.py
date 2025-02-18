import pandas as pd
import pickle
from typing import Any, Union
import os
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report


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

    def get_latest_version_from_registry(self):
        print("Current working directory:", os.getcwd())
        cwd = os.getcwd()
        files = os.listdir(f"{cwd}/registry")
        files = [file for file in files if ".pkl" in file]
        
        suffixes = [f.split('_v')[-1] for f in files]
        suffixes = [s.split('.')[0] for s in suffixes]

        print("Model versions in weights directory:", suffixes)
        try:
            latest_version = max([int(s) for s in suffixes])
        except Exception as e:
            latest_version = 0

        return latest_version

    def load_model(self) -> Union[Any, None]:
        """
        Load the model from the specified weights path.

        Returns:
            model (Any): The loaded model object, or None if loading fails.
        """
        try:
            # simulate getting latest versions from "model registry"
            latest_version = self.get_latest_version_from_registry()
            cwd = os.getcwd()
            if self.weights_path != "latest":
                # load a specific model version
                model = pickle.load(open(f"{cwd}/registry/{self.weights_path}", 'rb'))
            else:
                # default: load latest version
                model = pickle.load(open(f"{cwd}/registry/trained_pipeline_v{latest_version}.pkl", 'rb'))

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
    
    def create_model_pipeline(self):
        """
        Create the model pipeline.
        Returns:
            Sci-kit learn pipeline: The model pipeline with its components.
        """
        preprocessor = ColumnTransformer(
            transformers=[
                ('text_features', TfidfVectorizer(), 'transaction_details'), 
                ('numerical_features', Pipeline(
                    [
                        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
                        ('scaler', StandardScaler())
                    ]
                )
                , ['withdrawal_amt', 'deposit_amt', 'balance_amt', 'month', 'date_diff', 
                    'year', 'month_date', 'day', 'weekday', 'year_value_date', 'month_value_date', 
                    'day_value_date', 'weekday_value_date']),
                ('categorical_features', Pipeline(
                    [
                        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
                        ('onehot', OneHotEncoder(handle_unknown='ignore'))
                    ]
                ), ['account_id', 'city', 'device', 'transactionType'])
            ]
        )

        # Definir el pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier())
        ])

        return pipeline
    
    def tt_split(
            self,
            data: pd.DataFrame,
            test_size: float = 0.2,
            target_col: str = "target_category",
        ):
        
        X = data.drop(columns=[target_col])
        y = data[target_col]

        print("\n- Model Features after split:", X.columns.to_list())
        print("\n- Target column after split:", target_col)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
        
        return X_train, X_test, y_train, y_test
    
    def report_cross_val_score(
            self,
            model: Pipeline, 
            X_train: pd.DataFrame,
            y_train: pd.Series,
            report_metric: str = "accuracy"
            ) -> None:
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring=report_metric)
        cv_mean = np.mean(cv_scores)
        cv_std = np.std(cv_scores)

        print("\n====================================")
        print("Cross Validation Score")
        print("====================================\n")
        print(f"Mean CV Score ({report_metric}): {cv_mean}")
        print(f"Std CV Score ({report_metric}): {cv_std}")
        
    def report_classification_test_score(
            self,
            model: Pipeline,
            X_test: pd.DataFrame,
            y_test: pd.Series,
            X_train: pd.DataFrame,
            y_train: pd.Series,
        )-> None:
        print("\n> Reporting classification metrics on the Test Set")
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Report train and test accuracy to have an idea of potencial Overfitting
        print("\n====================================")
        print(f"Train Accuracy: {accuracy_score(y_train, y_pred_train)}")
        print(f"Test Accuracy: {accuracy_score(y_test, y_pred_test)}")
        print("====================================\n")

        # Report classification metrics on the test set
        report = classification_report(y_test, y_pred_test)
        print("==================================================================")
        print("                        Test Set Clasiffication Report")
        print("==================================================================\n")
        print(report)

    def save_model_to_registry(self, model: Pipeline, X_train: pd.DataFrame) -> None:
        """
        Save the model to the "model registry" (a local directory for this toy project).

        Parameters:
            model (Pipeline): The model to save.
        """
        try:
            cwd = os.getcwd()
            latest_version = self.get_latest_version_from_registry()
            new_version = latest_version + 1
            pickle.dump(model, open(f"{cwd}/registry/trained_pipeline_v{new_version}.pkl", 'wb'))
            print(f"Model saved to {cwd}/registry/trained_pipeline_v{new_version}.pkl")
            
            # TODO: Apply versioning to model features as well
            pd.DataFrame(X_train.columns.tolist()).to_csv(f"registry/model_features.csv", index= False, header=False)
        except Exception as e:
            print("Error saving model:", e)

    def train_classifier(self, raw_data: pd.DataFrame, report_cv_score: bool = False) -> Any:
        """
        Train the classifier on the input data.

        Parameters:
            raw_data (pd.DataFrame): Data from which training and testing splits will
                be created from.
        Returns:
            Any: Training results or an error message if not in training mode.
        """
        if self.mode == "training":
            print("\n====================================")
            print("Starting Model Training")
            print("====================================\n")

            # create the model bluepring and split the data
            model_pipeline = self.create_model_pipeline()
            X_train, X_test, y_train, y_test = self.tt_split(raw_data)
            y_train = np.array(y_train)
            y_test = np.array(y_test.values)

            # train the model
            model_pipeline.fit(X_train, y_train)

            # report cross val score
            if report_cv_score:
                self.report_cross_val_score(model=model_pipeline, X_train=X_train, y_train=y_train)
            
            # evaluate the model on the test set and report metrics.
            self.report_classification_test_score(
                model=model_pipeline,
                X_test=X_test,
                y_test=y_test,
                X_train=X_train,
                y_train=y_train,
            )
            # re train on all data

            # TODO for production only. for now, we are keeping the simpler 
            # training version since we are going to predict on test.
            
            # Save the model weights in the "registry" (a local dir for this toy project)
            self.save_model_to_registry(model_pipeline, X_train=X_train)
        else:
            return "Can't train model if not in training mode."