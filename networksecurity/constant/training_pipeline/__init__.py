import os

# =====================================================
# Pipeline level constants
# =====================================================
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR = "Artifacts"

# Target column (UCI dataset)
TARGET_COLUMN = "Result"

# =====================================================
# Raw dataset file names
# =====================================================

# UCI phishing dataset (tabular features)
FILE_NAME = "phisingData.csv"

# Raw URL dataset (text)
FILE_NAME_B = "url_data.csv"

# =====================================================
# Train / Test CSV files (Classical + Online ML)
# =====================================================
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

# (Optional backup for raw URL CSV – not required for DL)
TRAIN_FILE_NAME_B = "train2.csv"
TEST_FILE_NAME_B = "test2.csv"

# =====================================================
# Deep Learning tensor files (PyTorch)
# =====================================================
X_TRAIN_FILE = "X_train.pt"
Y_TRAIN_FILE = "y_train.pt"
X_TEST_FILE = "X_test.pt"
Y_TEST_FILE = "y_test.pt"

# =====================================================
# Model save paths
# =====================================================
SAVED_MODEL_DIR = os.path.join("saved_models")

# Classical ML
MODEL_FILE_NAME = "model.pkl"
SGD_MODEL_FILE_NAME = "sgd_model.pkl"
PA_MODEL_FILE_NAME = "passive_aggressive_model.pkl"

# Deep Learning
CNN_MODEL_FILE_NAME = "cnn_model.pt"
LSTM_MODEL_FILE_NAME = "lstm_model.pt"
RNN_MODEL_FILE_NAME = "rnn_model.pt"

# Optional
TABNET_MODEL_FILE_NAME = "tabnet_model.zip"

# =====================================================
# Schema
# =====================================================
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

# =====================================================
# Data Ingestion constants
# =====================================================
# MongoDB collections
DATA_INGESTION_UCI_COLLECTION = "NetworkData"
DATA_INGESTION_URL_COLLECTION = "URLTextData"

DATA_INGESTION_DATABASE_NAME = "NIDAF"

DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"

DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2
