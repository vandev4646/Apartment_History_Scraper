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
    listings = soup.find_all(class_=re.compile("listing-item column mcb-column one-third"))
    for item in listings:
        identifier =  "n/a"
        bed = bath = sqft = rent = 0
        
        identifier = item.find(class_="address").text.strip()
        bed = item.find(class_="beds").text.strip().split(" ")[0]
        bath = item.find(class_="baths").text.strip().split(" ")[0]
        sqft = item.find(class_="area").text.strip().split(" ")[0]
        rent = item.find(class_="rent-price-off").text.split()[1]
        formated_rent = float(rent.replace("$", "").replace(",", ""))
        data = (apartment.building, identifier, bed, bath, sqft, formated_rent, 1, formated_date)
        listing_data.append(data)

    #write data from all listings to the csv
    #csv_write(listing_data=listing_data, filename=apartment.filename)
    db_write(listing_data = listing_data)
    print(f'Write finished for {apartment.filename}')

def main():
    prairie = Apartment(
        "https://regencypm.com/prairie-crest-apartments-verona/",
        2, #"Regency Property Management Inc",
        8, #"Prairie Crest Apartments",
        3, #"Verona",
        f'Prairie_Crest_Listings_{formated_date}.csv'
    )
    lincoln = Apartment(
        "https://regencypm.com/lincoln-street-verona/",
        2, #"Regency Property Management Inc",
        7, #"Lincoln Street Apartments",
        3, #"Verona",
        f'Lincoln_Street_Listings_{formated_date}.csv'
    )
    courtyard = Apartment(
        "https://regencypm.com/courtyard-apartments-madison/",
        2, #"Regency Property Management Inc",
        3, #"Courtyard Apartments",
        2, #"Madison",
        f'Courtyard_Listings_{formated_date}.csv'
    )
    homestead = Apartment(
        "https://regencypm.com/homestead-luxury-rentals-verona/",
        2, #"Regency Property Management Inc",
        5, #"Homestead Luxury Apartments",
        3, #"Verona",
        f'Homestead_Luxury_Listings_{formated_date}.csv'
    )
    outlook = Apartment(
        "https://regencypm.com/the-outlook-at-1000-oaks-verona/",
        2, #"Regency Property Management Inc",
        10, #"The Outlook at 1000 Oaks Apartments",
        3, #"Verona",
        f'The_Outlook_Listings_{formated_date}.csv'
    )

    apartment_list = []
    apartment_list.append(prairie)
    apartment_list.append(lincoln)
    apartment_list.append(courtyard)
    apartment_list.append(homestead)
    apartment_list.append(outlook)
    print('Regeny Script')
    apartment_count = 0
    for apartment in apartment_list:
        apartment_data(apartment=apartment)
        apartment_count = apartment_count + 1

    print(f'Data was sucessfully written for {apartment_count} buildings')


if __name__=="__main__":
    main()