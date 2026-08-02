import csv
import os
import psycopg2

class Apartment():
    def __init__(self, url, company, building, city, filename):
        self.url = url
        self.company = company
        self.building = building
        self.city = city
        self.filename = filename

"""
parm: a tuple containing appartment data
This function writes the tuple data to a csv
"""
def csv_write(listing_data, filename):
    headers = [
    "Company", "Building", "City", "Identifier", "Bed", "Bath", "Sq Ft", "Rent Amount",
    "QTY", "Date Logged"
    ]
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerows(listing_data)

def db_write(listing_data):
    try:
        connection = psycopg2.connect(
            host = os.getenv("DB_HOST", "172.17.0.1"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()

        for item in listing_data:
            cursor.execute("""
            INSERT INTO listings (
                building_id, identifier, bed, bath, sq_ft, rent_amount, qty
            ) VALUES (%i, %s, %s, %s, %i, %f, %i);
        """, (
            item[0], item[1], item[2], item[3], item[4], item[5], item[6], 
        ))

        connection.commit()

    except Exception as e:
        if 'connection' in locals() and connection:
            connection.rollback()
        #update this to save to a local log file
        print(f"Error saving to database: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()