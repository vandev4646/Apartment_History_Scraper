from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import cloudscraper

from shared_utilities import Apartment, csv_write, db_write

#This program scraps data for the Lincoln Street Appartments in Verona
#NEED TO ADD ERROR HANDLING AND REPORT ON ERRORS



today = date.today()
formated_date = today.strftime("%m_%d_%Y")


"""
collects the following data points for each item
- Building
- Identifier (Address / Unit number if availabe otherwise the desription provided on site)
- Bed
- Bath
- Sq Ft
- Rent Amount
- QTY
- Date Logged
"""
def apartment_data(apartment: Apartment):
    listing_data = []
    URL = apartment.url
    scraper = cloudscraper.create_scraper()
    page = scraper.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    listings = soup.find_all(class_=re.compile("row row-eq-height vmiddle row-striped br"))
    print(listings)
    for item in listings:
        identifier = available = "n/a"
        bed = bath = sqft = rent = 0
        available = item.find(class_="avail-time").text.split()[0]
        if available != 'Not':
            identifier = item.find(class_="col-md-3 col-sm-12 col-xs-12 vmiddle text-center-sm text-center-xs").text.strip()
            size = item.find(class_="col-md-3 col-sm-6 col-xs-6 margin-bottom-sm margin-bottom-xs text-center").text.split()
            bed = size[1]
            bath = size[4]
            sqft = size[6]
            rent = item.find(class_="col-md-2 col-sm-6 col-xs-6 text-center").text.split()[1]
            formated_rent = float(rent.replace("$", "").replace(",", ""))
            data = (apartment.building, identifier, bed, bath, sqft, formated_rent, 1, formated_date)
            listing_data.append(data)

    #write data from all listings to the csv
    #csv_write(listing_data=listing_data, filename=apartment.filename)
    db_write(listing_data = listing_data)
    print(f'Write finished for {apartment.filename}')

def main():
    
    timber = Apartment(
        "https://www.mckenzie-apartments.com/properties/timber-valley/",
        1, #"McKenzie Apartment Company",
        11, #"Timber Valley Apartments",
        2, #"Madison",
        f'Timber_Valley_Listings_{formated_date}.csv'
    )
    whispering = Apartment(
        "https://www.mckenzie-apartments.com/properties/whispering-hills/",
        1, #"McKenzie Apartment Company",
        13, #"Whispering Hills Apartments",
        2, #"Madison",
        f'Whispering_Hills_Listings_{formated_date}.csv'
    )
    waterside = Apartment(
        "https://www.mckenzie-apartments.com/properties/waterside/",
        1, #"McKenzie Apartment Company",
        12, #"Waterside Apartments",
        2, #"Madison",
        f'Waterside_Listings_{formated_date}.csv'
    )
    siena = Apartment(
        "https://www.mckenzie-apartments.com/properties/siena-ridge/",
        1, #"McKenzie Apartment Company",
        9, #"Siena Ridge Apartments",
        3, #"Verona",
        f'Siena_Ridge_Listings_{formated_date}.csv'
    )
    legacy = Apartment(
        "https://www.mckenzie-apartments.com/properties/legacy-apartments/",
        1, #"McKenzie Apartment Company",
        6, #"Legacy Apartments",
        2, #"Madison",
        f'Legacy_Listings_{formated_date}.csv'
    )
    highland = Apartment(
        "https://www.mckenzie-apartments.com/properties/highland-ridge/",
        1, #"McKenzie Apartment Company",
        4, #"Highland Ridge Apartments",
        4, #"Middleton",
        f'Highland_Ridge_Listings_{formated_date}.csv'
    )
    boulder_creek = Apartment(
        "https://www.mckenzie-apartments.com/properties/boulder-creek/",
        1, #"McKenzie Apartment Company",
        2, #"Boulder Creek Apartments",
        2, #"Madison",
        f'Boulder_Creek_Listings_{formated_date}.csv'
    )
    blackhawk = Apartment(
        "https://www.mckenzie-apartments.com/properties/blackhawk-trails/",
        1, #"McKenzie Apartment Company",
        1, #"Blackhawk Trails Apartments",
        2, #"Madison",
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
    print("McKenzie Script")
    apartment_count = 0
    for apartment in apartment_list:
        apartment_data(apartment=apartment)
        apartment_count = apartment_count+1
    print(f'Data was sucessfully written for {apartment_count} buildings')


if __name__=="__main__":
    main()