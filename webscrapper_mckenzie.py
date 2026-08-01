from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import date
import csv
import os
import re

#This program scraps data for the Lincoln Street Appartments in Verona
#NEED TO ADD ERROR HANDLING AND REPORT ON ERRORS

class Apartment():
    def __init__(self, url, company, building, city, filename):
        self.url = url
        self.company = company
        self.building = building
        self.city = city
        self.filename = filename

today = date.today()
formated_date = today.strftime("%m_%d_%Y")

"""
parm: a tuple containing appartment data
This function writes the tuple data to a csv
"""
def csv_write(listing_data, filename):
    headers = [
    "Company", "Building", "City", "Identifier", "Bed", "Bath", "Sq Ft", "Available Date", "Rent Amount", "Application Fee",
    "Security Deposit", "Date Logged"
    ]
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerows(listing_data)

"""
collects the following data points for each item
- Company
- Building
- City
- Identifier (Address / Unit number if availabe otherwise the desription provided on site)
- Bed
- Bath
- Sq Ft
- Available Date
- Rent Amount
- Application Fee
- Security Deposit
- Date Logged
"""
def apartment_data(apartment: Apartment):
    listing_data = []
    URL = apartment.url
    page = requests.get(URL, impersonate="chrome")
    soup = BeautifulSoup(page.content, "lxml")
    listings = soup.find_all(class_=re.compile("row row-eq-height vmiddle row-striped br"))
    for item in listings:
        identifier = available = "n/a"
        bed = bath = sqft = rent = application_fee = security_deposit = 0
        available = item.find(class_="avail-time").text.split()[0]
        if available != 'Not':
            identifier = item.find(class_="col-md-3 col-sm-12 col-xs-12 vmiddle text-center-sm text-center-xs").text.strip()
            size = item.find(class_="col-md-3 col-sm-6 col-xs-6 margin-bottom-sm margin-bottom-xs text-center").text.split()
            bed = size[1]
            bath = size[4]
            sqft = size[6]
            rent = item.find(class_="col-md-2 col-sm-6 col-xs-6 text-center").text.split()[1]
            data = (apartment.company, apartment.building, apartment.city, identifier, bed, bath, sqft, available, rent,application_fee, security_deposit, formated_date)
            listing_data.append(data)

    #write data from all listings to the csv
    csv_write(listing_data=listing_data, filename=apartment.filename)

def main():
    
    timber = Apartment(
        "https://www.mckenzie-apartments.com/properties/timber-valley/",
        "McKenzie Apartment Company",
        "Timber Valley Apartments",
        "Madison",
        f'Timber_Valley_Listings_{formated_date}.csv'
    )
    whispering = Apartment(
        "https://www.mckenzie-apartments.com/properties/whispering-hills/",
        "McKenzie Apartment Company",
        "Whispering Hills Apartments",
        "Madison",
        f'Whispering_Hills_Listings_{formated_date}.csv'
    )
    waterside = Apartment(
        "https://www.mckenzie-apartments.com/properties/waterside/",
        "McKenzie Apartment Company",
        "Waterside Apartments",
        "Madison",
        f'Waterside_Listings_{formated_date}.csv'
    )
    siena = Apartment(
        "https://www.mckenzie-apartments.com/properties/siena-ridge/",
        "McKenzie Apartment Company",
        "Siena Ridge Apartments",
        "Verona",
        f'Siena_Ridge_Listings_{formated_date}.csv'
    )
    legacy = Apartment(
        "https://www.mckenzie-apartments.com/properties/legacy-apartments/",
        "McKenzie Apartment Company",
        "Legacy Apartments",
        "Madison",
        f'Legacy_Listings_{formated_date}.csv'
    )
    highland = Apartment(
        "https://www.mckenzie-apartments.com/properties/highland-ridge/",
        "McKenzie Apartment Company",
        "Highland Ridge Apartments",
        "Middleton",
        f'Highland_Ridge_Listings_{formated_date}.csv'
    )
    boulder_creek = Apartment(
        "https://www.mckenzie-apartments.com/properties/boulder-creek/",
        "McKenzie Apartment Company",
        "Boulder Creek Apartments",
        "Madison",
        f'Boulder_Creek_Listings_{formated_date}.csv'
    )
    blackhawk = Apartment(
        "https://www.mckenzie-apartments.com/properties/blackhawk-trails/",
        "McKenzie Apartment Company",
        "Blackhawk Trails Apartments",
        "Madison",
        f'Blackhawk_Trails_Listings_{formated_date}.csv'
    )

    apartment_list = []
    apartment_list.append(timber)
    apartment_list.append(whispering)
    apartment_list.append(waterside)
    apartment_list.append(siena)
    apartment_list.append(legacy)
    apartment_list.append(highland)
    apartment_list.append(boulder_creek)
    apartment_list.append(blackhawk)
    
    for apartment in apartment_list:
        apartment_data(apartment=apartment)


if __name__=="__main__":
    main()
