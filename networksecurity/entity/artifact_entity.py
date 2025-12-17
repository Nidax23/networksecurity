from dataclasses import dataclass
@dataclass
class UCIDataIngestionArtifact:
    trained_file_path: str
    test_file_path: str


@dataclass
class DLDataIngestionArtifact:
    X_train_path: str
    y_train_path: str
    X_test_path: str
    y_test_path: str
