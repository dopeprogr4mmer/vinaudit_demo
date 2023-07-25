import sqlite3
import pandas as pd 

def initialize_database():
    """
    Initializes and pre-populates the database
    Database name - vinaudit.db
    Table name - VINAUDIT
    """
    connection = sqlite3.connect('database/vinaudit.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS VINAUDIT;")

    csv_file = 'database/NEWTEST-inventory-listing-2022-08-17.txt'

    chunk_size = 100000
    chunks_list = []

    #Reading data in chunks
    for chunk in pd.read_csv(csv_file, sep='|', chunksize=chunk_size):
        chunks_list.append(chunk)
    
    df = pd.concat(chunks_list)

    df["vehicle"] = df['year'].astype(str) + " " + df['make'].astype(str) + " " + df['model'].astype(str)

    df["location"] = df["dealer_city"] + ", " + df["dealer_state"]

    df.to_sql('VINAUDIT', connection, index=False)

    #Creating indes on column 'vehicle' for faster queries 
    cursor.execute("CREATE INDEX idx_vehicle ON VINAUDIT (vehicle);")

    print("Inventory data dumped to table VINAUDIT")


if __name__ == "__main__":
	initialize_database()