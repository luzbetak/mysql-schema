from sqlalchemy import create_engine
import pandas as pd

#---------------------------------------------------------------------------------------------------#
# accepts a table name and retrieves information about the table, including its schema
#---------------------------------------------------------------------------------------------------#
def display_table_details(table_name):
    # Create a connection using SQLAlchemy
    engine_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(engine_url)

    # Query to get table schema
    schema_query = f"DESCRIBE {table_name}"
    schema_data = pd.read_sql(schema_query, engine)
    print(f"Schema for {table_name}:")
    print(schema_data)
    print()

    # Query to get table indexes
    index_query = f"SHOW INDEX FROM {table_name}"
    index_data = pd.read_sql(index_query, engine)
    print(f"Indexes for {table_name}:")
    print(index_data)
    print()

    # Query to get table partitioning details (if any)
    partition_query = f"SELECT * FROM information_schema.partitions WHERE TABLE_NAME = '{table_name}'"
    partition_data = pd.read_sql(partition_query, engine)
    print(f"Partitioning details for {table_name}:")
    print(partition_data)

#---------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    table_name = 'detection_series_data'  # Replace with the desired table name
    display_table_details(table_name)


