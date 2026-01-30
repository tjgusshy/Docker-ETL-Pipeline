# import necessary libraries

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import logging
import os
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w', filename='etl_pipeline.log')
                 


logger = logging.getLogger(__name__)

 
 






def run_pipeline():
    logger.info("Starting ETL pipeline...")
    # extract data
    try:
        data = {
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'role': ['Engineer', 'Doctor', 'Artist'],
            'ingested_at': [datetime.datetime.now()] * 3
        }
        df = pd.DataFrame(data)
        logger.info(f"Data extracted successfully: {df.shape[0]} records.")
        
    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
        return
    # accessing database credentials from environment variables
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = os.getenv('DB_PORT')  

    #check if any of the credentials are missing

    if not all([db_host, db_name, db_user, db_password, db_port]):
        logger.error("Database credentials are not fully set in environment variables.")
        return

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    # loading data into the database
    try:
        logger.info(f"connecting to the database at {db_host}:{db_port}/{db_name}...")
        engine = create_engine(connection_string)
        df.to_sql('employees', engine, if_exists='replace', index=False)
        logger.info("Data loaded into the database successfully.")
    except Exception as e:
        logger.error(f"Error loading data into the database: {e}")
        return
    
if __name__ == "__main__":
    run_pipeline()