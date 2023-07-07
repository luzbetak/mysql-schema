#!/usr/bin/env python3 
#----------------------------------------------------------------------------------------------#
import pandas as pd
from mysql.connector import connect
import logging  # Make sure this line is here

#----------------------------------------------------------------------------------------------#
DB_SETTINGS = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "database"
}
#----------------------------------------------------------------------------------------------#
# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler which logs info messages
fh = logging.FileHandler('data-sampling.log')
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

#----------------------------------------------------------------------------------------------#
def get_table_names():
    conn = connect(**DB_SETTINGS)
    cursor = conn.cursor()

    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    finally:
        cursor.close()
        conn.close()

#----------------------------------------------------------------------------------------------#
def select_vertical(table_name):
    conn = connect(**DB_SETTINGS)
    cursor = conn.cursor(dictionary=True)

    try:
        # Query to fetch the data
        sql_query = f"""
                    SELECT *
                    FROM `{table_name}`
                    ORDER BY RAND()
                    LIMIT 1;
                    """
        cursor.execute(sql_query)

        # Fetch the data and convert to DataFrame
        records = cursor.fetchall()
        df = pd.DataFrame(records)

        # Set pandas options
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)

        if 'created' in df.columns:
            df.sort_values(by='created', inplace=True, ignore_index=True)

        # Iterate over all records and print them
        for i in range(df.shape[0]):
            record = df.iloc[i].transpose()
            logger.info(f"Record {i + 1} from table '{table_name}':")
            for index, value in record.items():
                logger.info(f"{index:<50} {str(value)[:200]}")
            logger.info('-' * 100)  # Empty line

    finally:
        cursor.close()
        conn.close()

#----------------------------------------------------------------------------------------------#
if __name__ == "__main__":  

    table_names = get_table_names()
    for table in table_names:
        select_vertical(table)

