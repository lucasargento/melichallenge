from components.preprocessor import Preprocessor
from components.pipeline import ClassificationPipeline
from components.bq_connector import BatchFetcher

def run_inference():
    '''
    Runs batch inference from a specific data source.
    '''
    try:
        # initialize components
        batchFetcher = BatchFetcher()
        preprocessor = Preprocessor()
        predictor = ClassificationPipeline()
        
        print("\n\n============================")
        print("Starting Inference Pipeline")
        print("============================\n\n")

        # pipeline steps
        raw_data = batchFetcher.load_data()
        preprocessed_data = preprocessor.preprocess(raw_data)
        predictions = predictor.run_batch_pred(preprocessed_data)

        print("\n\nPredictions array:", predictions)
        preprocessed_data["predictions"] = predictions
        batchFetcher.write_to_bq(preprocessed_data, "predictions")
        
        print("\n\n========================================================")
        print("Inference Pipeline Completed Succesfully")
        print("========================================================")

        return predictions
    except Exception as e:
        print("Error during pipeline execution:", e)
        return None
    
if __name__ == "__main__":
    run_inference()