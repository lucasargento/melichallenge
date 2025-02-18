from components.preprocessor import Preprocessor
from components.classifier import ClassificationPipeline
from components.bq_connector import BatchFetcher
import time

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
    start_time = time.time()
    run_inference()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed training time: {elapsed_time:.2f} seconds")