import os,sys
from src.intel.configuration.s3_opearations import S3Sync
from src.intel.logger import logging
from src.intel.exception import CustomException
from src.intel.constants import *
from src.intel.entity.artifact_entity import *
from src.intel.utils import *

class ModelPusher:
    def __init__(self, model_evaluation_artifacts: ModelEvaluationArtifacts):
        self.model_evaluation_artifacts = model_evaluation_artifacts

    def initiate_model_pusher(self):
        try:
            logging.info("Initiating model pusher component")
            if self.model_evaluation_artifacts.is_model_accepted:
                trained_model_path = self.model_evaluation_artifacts.trained_model_path
                s3_model_folder_path = self.model_evaluation_artifacts.s3_model_path
                s3_sync = S3Sync()
                s3_sync.sync_folder_to_s3(folder=trained_model_path, aws_bucket_url=s3_model_folder_path)
                message = "Model Pusher pushed the current Trained model to Production server storage"
                response = {"is model pushed": True, "S3_model": s3_model_folder_path + "/" + str(MODEL_NAME),"message" : message}
                logging.info(response)
            else:
                s3_model_folder_path = self.model_evaluation_artifacts.s3_model_path
                message = "Current Trained Model is not accepted as model in Production has better loss"
                response = {"is model pushed": False, "S3_model":s3_model_folder_path,"message" : message}
                logging.info(response)
            model_pusher_artifacts = ModelPusherArtifacts(response=response)
            logging.info(f"Model evaluation completed! Artifacts: {model_pusher_artifacts}")
            logging.info("model training completed")
        except Exception as e:
            raise CustomException(e, sys)