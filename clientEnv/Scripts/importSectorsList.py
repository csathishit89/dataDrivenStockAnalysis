import psycopg2
from pathlib import Path
import pandas as pd
import io # Used to treat the CSV data like a file object
import hashlib
import csv
import connectionInfo

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE_PATH = BASE_DIR / "Sector_data.csv"

TABLE_NAME = "sector"

def insert_data_from_csv(csv_path, table_name):
    """
    Connects to PostgreSQL and uses the COPY FROM method 
    to quickly upload data from a CSV file.
    """
    try:
        # Establish connection
        cur = connectionInfo.conn.cursor()
        
        insert_query = f"""
            INSERT INTO {table_name} (company_name, sector_name, symbol)
            VALUES (%s, %s, %s)
        """
        data_to_insert = []
         
        # 2. Read the CSV file and prepare data for insertion
        with open(csv_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            
            for row in reader:
                getSymbol = row[2]
                parts = getSymbol.split(':')
                fetchSymbol = [part.strip() for part in parts] 
            
                row_data = (row[0], row[1], fetchSymbol[1])
                data_to_insert.append(row_data)

        if data_to_insert:
            # 3. Execute the batch insert
            cur.executemany(insert_query, data_to_insert)
            connectionInfo.conn.commit()
            print(f"✅ Successfully inserted {len(data_to_insert)} rows into {table_name}.")
            
    except (Exception, psycopg2.Error) as error:
        print(f"❌ Error while connecting to PostgreSQL or inserting data: {error}")
    finally:
        # Close the database connection
        if connectionInfo.conn:
            cur.close()
            connectionInfo.conn.close()

insert_data_from_csv(CSV_FILE_PATH, TABLE_NAME)