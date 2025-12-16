import psycopg2
from pathlib import Path
import pandas as pd
import io # Used to treat the CSV data like a file object
import hashlib
import csv
import connectionInfo

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE_PATH = BASE_DIR / "final_output.csv"

TABLE_NAME = "stocks"

def insert_data_from_csv(csv_path, table_name):
    """
    Connects to PostgreSQL and uses the COPY FROM method 
    to quickly upload data from a CSV file.
    """
    try:
        # Establish connection
        cur = connectionInfo.conn.cursor()
        
        insert_query = f"""
            INSERT INTO {table_name} (sectorid, close_price, stock_datetime, high, low,month, open, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_to_insert = []
         
        # 2. Read the CSV file and prepare data for insertion
        with open(csv_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            count = 0
            for row in reader:
                count += 1
                symbol_value = row[0]
                cur.execute("SELECT sectorid FROM public.sector WHERE symbol = %s order by sectorid desc", (row[0],))
                result = cur.fetchall()
                
                if not result:
                    print(f"⚠️ Warning: No sectorid found for symbol '{symbol_value}'. Skipping this row.")
                    continue # Skip to the next row in the CSV
            
                sector_id = result[0][0]
                row_data = (sector_id, row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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