from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import date
import csv
import os

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
parm: the url of the list you want to scrap data for
returns: An tuple with the following data points
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
def list_data(url, company, building, city):
    #get the data from the listing page
    identifier = available = "n/a"
    bed = bath = sqft = rent = application_fee = security_deposit = 0
    page = requests.get(url, impersonate="chrome")
    soup = BeautifulSoup(page.content, "lxml")
    #extract all the needed fields
    item = soup.find(class_="address-hdng")
    if item.contents == []: return ("", "", "", "", "", "", "", "", "","", "", "")
    identifier = item.contents[0].strip()
    bbs = soup.find(class_="bed-bath-std").find_all("span")
    bslen = len(bbs)
    if bslen >= 1:
        bed = bbs[0].text.strip().split()[0]
    if bslen >= 2:
        bath = bbs[1].text.strip().split()[0]
    if bslen >= 3:
        sqft = bbs[2].text.strip().split()[1]
    if bslen >= 4:
        available = bbs[3].text.strip().split()[2]
    list_items = soup.find_all(class_="list__item")
    rent = list_items[0].text.split()[1]
    application_fee = list_items[1].text.split()[2]
    security_deposit = list_items[2].text.split()[2]

    #return all the data fields collected as a tuple
    return(company, building, city, identifier, bed, bath, sqft, available, rent,application_fee, security_deposit, formated_date)

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

def apartment_data(apartment: Apartment):
    URL = apartment.url
    page = requests.get(URL, impersonate="chrome")
    soup = BeautifulSoup(page.content, "lxml")
    
    #get all the url's on the page and select the ones assoicated with details
    urls = [tag['href'] for tag in soup.find_all(class_="more_detail_btn")]
    listing_data = []
    
    #get the data for each listing
    for url in urls:
        listing_data.append(list_data(url=url, company=apartment.company, building=apartment.building, city=apartment.city))
    #write data from all listings to the csv
    csv_write(listing_data=listing_data, filename=apartment.filename)

def main():
    prairie = Apartment(
        "https://regencypm.com/prairie-crest-apartments-verona/",
        "Regency Property Management Inc",
        "Prairie Crest Apartments",
        "Verona",
        f'Prairie_Crest_Listings_{formated_date}.csv'
    )
    lincoln = Apartment(
        "https://regencypm.com/lincoln-street-verona/",
        "Regency Property Management Inc",
        "Lincoln Street Apartments",
        "Verona",
        f'Lincoln_Street_Listings_{formated_date}.csv'
    )
    courtyard = Apartment(
        "https://regencypm.com/courtyard-apartments-madison/",
        "Regency Property Management Inc",
        "Courtyard Apartments",
        "Madison",
        f'Courtyard_Listings_{formated_date}.csv'
    )
    homestead = Apartment(
        "https://regencypm.com/homestead-luxury-rentals-verona/",
        "Regency Property Management Inc",
        "Homestead Luxury Apartments",
        "Verona",
        f'Homestead_Luxury_Listings_{formated_date}.csv'
    )
    outlook = Apartment(
        "https://regencypm.com/the-outlook-at-1000-oaks-verona/",
        "Regency Property Management Inc",
        "The Outlook at 1000 Oaks Apartments",
        "Verona",
        f'The_Outlook_Listings_{formated_date}.csv'
    )

    apartment_list = []
    apartment_list.append(prairie)
    apartment_list.append(lincoln)
    apartment_list.append(courtyard)
    apartment_list.append(homestead)
    apartment_list.append(outlook)

    for apartment in apartment_list:
        apartment_data(apartment=apartment)


if __name__=="__main__":
    main()
