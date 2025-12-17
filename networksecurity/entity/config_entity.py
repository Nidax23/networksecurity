from datetime import datetime
import os
from networksecurity.constant import training_pipeline
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp

# =====================================================
# Data Ingestion Config
# =====================================================
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Base ingestion directory
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # ============================
        # UCI Tabular Data (ML / Online ML)
        # ============================
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.testing_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        # ============================
        # Raw URL CSV backup (optional)
        # ============================
        self.feature_store_file_path_b = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME_B
        )

        self.training_file_path_b = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME_B
        )

        self.testing_file_path_b = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME_B
        )

        # ============================
        # Deep Learning (PyTorch tensors)
        # ============================
        self.dl_data_dir = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            "dl"
        )

        self.X_train_path = os.path.join(self.dl_data_dir, training_pipeline.X_TRAIN_FILE)
        self.y_train_path = os.path.join(self.dl_data_dir, training_pipeline.Y_TRAIN_FILE)
        self.X_test_path = os.path.join(self.dl_data_dir, training_pipeline.X_TEST_FILE)
        self.y_test_path = os.path.join(self.dl_data_dir, training_pipeline.Y_TEST_FILE)

        # ============================
        # MongoDB
        # ============================
        self.uci_collection_name = training_pipeline.DATA_INGESTION_UCI_COLLECTION
        self.url_collection_name = training_pipeline.DATA_INGESTION_URL_COLLECTION
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME

        # ============================
        # Common parameters
        # ============================
        self.train_test_split_ratio = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        )
