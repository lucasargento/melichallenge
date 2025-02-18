from components.preprocessor import Preprocessor
from components.classifier import ClassificationPipeline
from components.bq_connector import BatchFetcher
import time

def run_training():
    '''
    Runs batch inference from a specific data source.
    '''
    try:
        # initialize components
        batchFetcher = BatchFetcher(mode="training")
        preprocessor = Preprocessor(mode="training")
        predictor = ClassificationPipeline(mode="training")

        
        print("\n\n============================")
        print("Starting Training Pipeline")
        print("============================\n\n")

        # pipeline steps
        raw_data = batchFetcher.load_data()
        preprocessed_data = preprocessor.preprocess(raw_data)
        predictor.train_classifier(preprocessed_data, report_cv_score=True)
        
        print("\n\n========================================================")
        print("Training Pipeline Completed Succesfully")
        print("========================================================")

        return True
    except Exception as e:
        print("Error during pipeline execution:", e)
        return False
    
if __name__ == "__main__":
    start_time = time.time()
    run_training()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed training time: {elapsed_time:.2f} seconds")