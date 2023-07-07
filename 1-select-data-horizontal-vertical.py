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
def select_vertical():

    conn = connect(**DB_SETTINGS)
    cursor = conn.cursor(dictionary=True)

    try:
        # Query to fetch the data
        sql_query = """
                    SELECT *
                    FROM database.table 
                    ORDER BY created DESC 
                    LIMIT 5;
                    """

        cursor.execute(sql_query)

        # Fetch the data and convert to DataFrame
        klines = cursor.fetchall()
        df = pd.DataFrame(klines)

        # Set pandas options
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        df.sort_values(by='created', inplace=True, ignore_index=True)

        # Iterate over all records and print them
        for i in range(df.shape[0]):
            record = df.iloc[i].transpose()
            print(f"Record {i + 1}:")
            for index, value in record.items():
                print(f"{index:<50} {str(value)[:200]}")
            print('-' * 100)  # Empty line

    finally:
        cursor.close()
        conn.close()

#----------------------------------------------------------------------------------------------#
def select_horizontal():

    conn = connect(**DB_SETTINGS)
    cursor = conn.cursor(dictionary=True)

    try:
        # Query to fetch the data
        sql_query = """ 
                    SELECT * 
                    FROM database.table 
                    ORDER BY RAND()
                    LIMIT 40;
                    """

        cursor.execute(sql_query)

        # Fetch the data and convert to DataFrame
        klines = cursor.fetchall()
        df = pd.DataFrame(klines)

        # Set pandas options
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.max_colwidth', None)  # Add this line
        df.sort_values(by='created', inplace=True, ignore_index=True)
        print(df)

    finally:
        cursor.close()
        conn.close()


#----------------------------------------------------------------------------------------------#
if __name__ == "__main__":

    select_vertical()
    select_horizontal()

    
