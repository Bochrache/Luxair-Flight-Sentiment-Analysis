import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_PATH = os.getenv("DB_PATH")
DB_FILE_NAME = os.getenv("DB_FILE_NAME")

def initialize_database():
    """
    Initializes the SQLite database and creates the necessary tables
    for flights and reviews based on the defined schema.
    """
    if not DB_PATH or not DB_FILE_NAME:
        print("Error: DB_PATH or DB_FILE_NAME not found in .env file.")
        return

    # Ensure the directory for the database exists
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create flights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                flight_id TEXT PRIMARY KEY,
                flight_icao TEXT NOT NULL,
                flight_iata TEXT,
                airline_icao TEXT NOT NULL,
                airline_iata TEXT,
                dep_airport_icao TEXT NOT NULL,
                dep_airport_iata TEXT,
                arr_airport_icao TEXT NOT NULL,
                arr_airport_iata TEXT,
                dep_scheduled DATETIME,
                dep_estimated DATETIME,
                dep_actual DATETIME,
                arr_scheduled DATETIME,
                arr_estimated DATETIME,
                arr_actual DATETIME,
                dep_delay INTEGER,
                arr_delay INTEGER,
                status TEXT,
                aircraft_icao TEXT,
                aircraft_iata TEXT,
                last_updated DATETIME NOT NULL
            );
        """)

        # Create reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_text TEXT NOT NULL,
                overall_rating INTEGER,
                recommended BOOLEAN,
                trip_verified BOOLEAN,
                review_date DATE,
                route TEXT,
                type_of_traveller TEXT,
                seat_type TEXT,
                aircraft TEXT,
                seat_comfort_rating INTEGER,
                cabin_staff_rating INTEGER,
                food_beverages_rating INTEGER,
                ground_service_rating INTEGER,
                value_for_money_rating INTEGER,
                inflight_entertainment_rating INTEGER,
                wifi_connectivity_rating INTEGER,
                sentiment_score REAL,
                sentiment_label TEXT
            );
        """)

        conn.commit()
        print(f"Database '{DB_FILE_NAME}' initialized successfully with 'flights' and 'reviews' tables.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_database()
