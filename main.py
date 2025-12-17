from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig
)
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging


def main():
    logging.info("Starting Network Security Pipeline")

    # 1️⃣ Create pipeline-level config
    pipeline_config = TrainingPipelineConfig()

    # 2️⃣ Create data ingestion config
    ingestion_config = DataIngestionConfig(pipeline_config)

    # =====================================================
    # CASE 1: Classical ML / Online ML (SGD, PA, RF)
    # =====================================================
    logging.info("Running UCI tabular data ingestion")

    uci_ingestion = DataIngestion(
        data_ingestion_config=ingestion_config,
        dataset_type="uci_tabular"
    )

    uci_artifact = uci_ingestion.initiate_data_ingestion()

    logging.info(f"UCI Train CSV: {uci_artifact.trained_file_path}")
    logging.info(f"UCI Test CSV: {uci_artifact.test_file_path}")

    # =====================================================
    # CASE 2: Deep Learning (CNN / RNN / LSTM)
    # =====================================================
    logging.info("Running URL text data ingestion")

    url_ingestion = DataIngestion(
        data_ingestion_config=ingestion_config,
        dataset_type="url_text",
        model_type="cnn",      # change to rnn / lstm if needed
        max_len=150
    )

    url_artifact = url_ingestion.initiate_data_ingestion()

    logging.info(f"X_train.pt: {url_artifact.X_train_path}")
    logging.info(f"y_train.pt: {url_artifact.y_train_path}")
    logging.info(f"X_test.pt: {url_artifact.X_test_path}")
    logging.info(f"y_test.pt: {url_artifact.y_test_path}")

    logging.info("Data ingestion completed successfully")


if __name__ == "__main__":
    main()
