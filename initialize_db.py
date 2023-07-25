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
    
    df = pd.read_csv("database/NEWTEST-inventory-listing-2022-08-17.txt", sep='|')

    # print(df.columns)

    df["vehicle"] = df['year'].astype(str) + " " + df['make'].astype(str) + " " + df['model'].astype(str)

    df["location"] = df["dealer_city"] + ", " + df["dealer_state"]

    df.to_sql('VINAUDIT', connection, index=False)

    cursor.execute("CREATE INDEX idx_vehicle ON VINAUDIT (vehicle);")

    print("Inventory data dumped to table VINAUDIT")


if __name__ == "__main__":
	initialize_database()