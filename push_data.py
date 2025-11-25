import os
import sys
import json
from dotenv import load_dotenv
import pandas as pd
import pymongo
import certifi

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print("Mongo URL:", MONGO_DB_URL)

ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            # You can initialize shared things here if needed
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        """
        Reads a CSV file and converts it to a list of JSON-like dict records.
        """
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            # Convert DataFrame to list of dicts
            records = data.to_dict(orient="records")
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        """
        Inserts a list of records into MongoDB.
        """
        try:
            db = self.mongo_client[database]
            coll = db[collection]

            result = coll.insert_many(records)
            return len(result.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = r"Network_data\phisingData.csv"


    DATABASE = "NIDAF"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()

   
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(f"Total records read from CSV: {len(records)}")

    print( records)

    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)
