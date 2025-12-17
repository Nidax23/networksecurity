from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import (
    UCIDataIngestionArtifact,
    DLDataIngestionArtifact
)
from networksecurity.constant.training_pipeline import TARGET_COLUMN
import os
import sys
import numpy as np
import pandas as pd
import pymongo
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(
        self,
        data_ingestion_config: DataIngestionConfig,
        dataset_type: str = "uci_tabular",   # uci_tabular | url_text
        model_type: str = None,              # cnn | rnn | lstm
        max_len: int = 150
    ):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.dataset_type = dataset_type
            self.model_type = model_type
            self.max_len = max_len
            self.scaler = MinMaxScaler()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =====================================================
    # COMMON: Load data from MongoDB (COLLECTION-AWARE)
    # =====================================================
    def export_collection_as_dataframe(self):
        try:
            client = pymongo.MongoClient(MONGO_DB_URL)

            if self.dataset_type == "uci_tabular":
                collection_name = self.data_ingestion_config.uci_collection_name
            else:
                collection_name = self.data_ingestion_config.url_collection_name

            collection = client[
                self.data_ingestion_config.database_name
            ][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)
            df.dropna(inplace=True)

            logging.info(
                f"Loaded data from MongoDB | Collection: {collection_name} | "
                f"Columns: {df.columns.tolist()}"
            )
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =====================================================
    # DATASET 1: UCI TABULAR DATA (SGD / PA / RF)
    # =====================================================
    from networksecurity.constant.training_pipeline import TARGET_COLUMN

    def ingest_uci_tabular_data(self, dataframe: pd.DataFrame):
       try:
        logging.info("Starting UCI tabular data ingestion")

        X = dataframe.drop(TARGET_COLUMN, axis=1)
        y = dataframe[TARGET_COLUMN]

        X_scaled = self.scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled,
            y,
            test_size=self.data_ingestion_config.train_test_split_ratio,
            random_state=42,
            stratify=y
        )

        os.makedirs(
            os.path.dirname(self.data_ingestion_config.training_file_path),
            exist_ok=True
        )

        train_df = pd.DataFrame(X_train, columns=X.columns)
        train_df[TARGET_COLUMN] = y_train.values

        test_df = pd.DataFrame(X_test, columns=X.columns)
        test_df[TARGET_COLUMN] = y_test.values

        train_df.to_csv(self.data_ingestion_config.training_file_path, index=False)
        test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False)

        logging.info("UCI tabular ingestion completed")

        return UCIDataIngestionArtifact(
            trained_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path
        )

       except Exception as e:
          raise NetworkSecurityException(e, sys)

    # =====================================================
    # DATASET 2: RAW URL DATA (CNN / RNN / LSTM)
    # =====================================================
    def ingest_url_sequence_data(self, dataframe: pd.DataFrame):
        try:
            logging.info("Starting URL sequence ingestion (PyTorch)")

            # Validate schema
            if "url" not in dataframe.columns or "type" not in dataframe.columns:
                raise ValueError(
                    f"Expected ['url', 'type'], found {dataframe.columns.tolist()}"
                )

            urls = dataframe["url"].astype(str).values

            # Convert categorical label → binary
            dataframe["label"] = dataframe["type"].str.lower().apply(
                lambda x: 0 if x == "benign" else 1
            )
            labels = dataframe["label"].values

            logging.info("Converted URL types to binary labels")

            # Character-level vocabulary
            chars = sorted(list(set("".join(urls))))
            char_to_idx = {ch: i + 1 for i, ch in enumerate(chars)}  # 0 = padding

            def encode_url(url):
                encoded = [char_to_idx.get(c, 0) for c in url[:self.max_len]]
                if len(encoded) < self.max_len:
                    encoded += [0] * (self.max_len - len(encoded))
                return encoded

            X = np.array([encode_url(url) for url in urls])
            y = np.array(labels)

            # Convert to tensors
            X = torch.tensor(X, dtype=torch.long)
            y = torch.tensor(y, dtype=torch.long)

            # CNN-specific reshape
            if self.model_type == "cnn":
                X = X.unsqueeze(1)

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42,
                stratify=y
            )

            os.makedirs(self.data_ingestion_config.dl_data_dir, exist_ok=True)

            X_train_path = self.data_ingestion_config.X_train_path
            y_train_path = self.data_ingestion_config.y_train_path
            X_test_path = self.data_ingestion_config.X_test_path
            y_test_path = self.data_ingestion_config.y_test_path

            torch.save(X_train, X_train_path)
            torch.save(y_train, y_train_path)
            torch.save(X_test, X_test_path)
            torch.save(y_test, y_test_path)

            logging.info("PyTorch tensors saved successfully")

            return DLDataIngestionArtifact(
                X_train_path=X_train_path,
                y_train_path=y_train_path,
                X_test_path=X_test_path,
                y_test_path=y_test_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =====================================================
    # PIPELINE ENTRY POINT
    # =====================================================
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()

            if self.dataset_type == "uci_tabular":
                return self.ingest_uci_tabular_data(dataframe)

            elif self.dataset_type == "url_text":
                return self.ingest_url_sequence_data(dataframe)

            else:
                raise ValueError(
                    "dataset_type must be 'uci_tabular' or 'url_text'"
                )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
