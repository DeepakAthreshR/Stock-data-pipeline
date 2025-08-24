# This script contains the core logic for the data pipeline:
# 1. Fetching data from a stock market API.
# 2. Connecting to a PostgreSQL database.
# 3. Storing the data in a table.

import requests
import psycopg2
import os
import logging
import json
from datetime import datetime

# Configure logging for better visibility and debugging.
logging.basicConfig(level=logging.INFO)

# --- Configuration using Environment Variables ---
DB_HOST = os.getenv('AIRFLOW_VAR_DB_HOST', 'postgres')
DB_NAME = 'stock_data'
DB_USER = 'stock_user'
DB_PASSWORD = 'stock_password'
STOCK_API_KEY = os.getenv('AIRFLOW_VAR_STOCK_API_KEY')
STOCK_SYMBOL = 'AAPL' # Example stock symbol

# --- Database Operations ---

def create_table_if_not_exists():
    """
    Connects to the PostgreSQL database and creates the stock_data table
    if it does not already exist.
    """
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        logging.info("Successfully connected to the PostgreSQL database.")

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS stock_data (
            symbol VARCHAR(10) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            volume INT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            PRIMARY KEY (symbol, timestamp)
        );
        """
        cur.execute(create_table_sql)
        conn.commit()
        logging.info("Table 'stock_data' checked/created successfully.")
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error creating table: {error}")
    finally:
        if conn is not None:
            conn.close()

def insert_stock_data(symbol, price, volume):
    """
    Inserts a single stock data record into the 'stock_data' table.
    """
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        logging.info("Database connection for insertion successful.")

        insert_sql = """
        INSERT INTO stock_data (symbol, price, volume, timestamp)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (symbol, timestamp) DO NOTHING;
        """
        
        cur.execute(insert_sql, (symbol, price, volume, datetime.now()))
        conn.commit()
        logging.info(f"Successfully inserted data for {symbol}.")
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error inserting data into table: {error}")
    finally:
        if conn is not None:
            conn.close()

# --- API Interaction and Data Extraction ---

def fetch_and_store_stock_data():
    """
    Main function to orchestrate the data fetching and storage.
    This function will be called by the Airflow task.
    """
    logging.info("Starting data fetching and storage process...")

    if not STOCK_API_KEY:
        logging.error("STOCK_API_KEY is not set. Please check your environment variables.")
        return

    # Using the Alpha Vantage API as an example
    # Replace with a real API like Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={STOCK_SYMBOL}&apikey={STOCK_API_KEY}' 

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info("Successfully fetched data from API.")

        # --- Data Extraction ---
        # Assuming the API response has a specific structure.
        quote_data = data.get('Global Quote', {})
        price = quote_data.get('05. price')
        volume = quote_data.get('06. volume')
        
        if not price or not volume:
            logging.warning("Missing 'price' or 'volume' in API response. Skipping insertion.")
            logging.debug(f"Received data: {data}")
            return

        try:
            price = float(price)
            volume = int(volume)
        except (ValueError, TypeError) as e:
            logging.error(f"Failed to convert data types: {e}. Raw data: price={price}, volume={volume}")
            return
            
        insert_stock_data(STOCK_SYMBOL, price, volume)

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data from API: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Failed to parse API response: {e}")

if __name__ == "__main__":
    create_table_if_not_exists()
    fetch_and_store_stock_data()
