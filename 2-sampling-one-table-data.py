#!/usr/bin/env python3 
#----------------------------------------------------------------------------------------------#
import datetime, os, time, calendar
from mysql.connector import connect, Error
from pprint import pprint
import pandas as pd

#----------------------------------------------------------------------------------------------#
DB_SETTINGS = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "database"
}
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
            print(f"Record {i + 1} from table '{table_name}':")
            for index, value in record.items():
                print(f"{index:<50} {str(value)[:200]}")
            print('-' * 100)  # Empty line

    finally:
        cursor.close()
        conn.close()

#----------------------------------------------------------------------------------------------#
if __name__ == "__main__":  
    table_names = get_table_names()
    for table in table_names:
        select_vertical(table)


