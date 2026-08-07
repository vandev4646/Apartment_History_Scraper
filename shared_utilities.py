import csv
from datetime import date, timedelta
from decimal import Decimal
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
    "Building", "Identifier", "Bed", "Bath", "Sq Ft", "Rent Amount",
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
    
            today = date.today()
            yesterday = today - timedelta(days=1)
            date_31 = today - timedelta(days=31)
            date_61 = today - timedelta(days=61)
    
            num_listings = len(listing_data)
            total_days_vacant = 0
            building_id = listing_data[0][0]
            print("Building_ID")
            print(building_id)
    
            for item in listing_data:
                cursor.execute("""
                SELECT COALESCE(MAX(days_vacant), 0) 
                FROM listings 
                WHERE date_logged = %s AND identifier = %s;""", (yesterday, item[1]))
    
                days_vacant = (cursor.fetchone()[0])+1;
                total_days_vacant +=days_vacant
    
                cursor.execute("""
                INSERT INTO listings (
                    building_id, identifier, bed, bath, sq_ft, rent_amount, qty, days_vacant
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (item[0], item[1], item[2], item[3], item[4], item[5], item[6], days_vacant))
    
            #INSERT INTO SUMMARY TABLE
            average_vacant = Decimal(total_days_vacant) / Decimal(num_listings)
            #note if there is no 30 or 60 day for yesterday then set it equal to today
            cursor.execute("""SELECT COALESCE(MAX(units_30), %s), COALESCE(MAX(units_60), %s), COALESCE(MAX(vacant_30), %s), COALESCE(MAX(vacant_60), %s) FROM summary WHERE date_logged = %s AND building_id = %s;""", (num_listings, num_listings, average_vacant, average_vacant, yesterday, building_id))
            items = cursor.fetchone()
            units_30 = items[0]
            units_60 = items[1]
            vacant_30 = items[2]
            vacant_60 = items[3]
    
            cursor.execute("""SELECT units_available, days_vacant FROM summary WHERE date_logged = %s AND building_id = %s;""", (date_31, building_id))
            items = cursor.fetchone()
            if items is None:
                vacant_30 = average_vacant
                units_30 = num_listings
            else:
                units_31 = items[0]
                vacant_31 = items[1]
                vacant_30 = vacant_30 + ((average_vacant-vacant_31)/30)
                units_30 = units_30 + ((num_listings-units_31)/30)
                
    
            cursor.execute("""
            SELECT units_available, days_vacant 
            FROM summary 
            WHERE date_logged = %s AND building_id = %s;
            """, (date_61, building_id))
    
            items = cursor.fetchone()
            if items is None:
                vacant_60 = average_vacant
                units_60 = num_listings
            else:
                units_61 = items[0]
                vacant_61 = items[1]    
            
                units_60 = units_60 + ((num_listings-units_61)/30)
                vacant_60 = vacant_60 + ((average_vacant-vacant_61)/30)
    
            
    
            cursor.execute("""
            INSERT INTO summary(
            date_logged, building_id, units_available, units_30, units_60, days_vacant, vacant_30, vacant_60
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (today, building_id, num_listings, units_30, units_60, average_vacant, vacant_30, vacant_60))
    
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