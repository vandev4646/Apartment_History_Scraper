from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import date

from shared_utilities import Apartment, csv_write, db_write

#This program scraps data for the Lincoln Street Appartments in Verona
#NEED TO ADD ERROR HANDLING AND REPORT ON ERRORS

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
- Rent Amount
- QTY
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
    list_items = soup.find_all(class_="list__item")
    rent = list_items[0].text.split()[1]
    formated_rent = float(rent.replace("$", "").replace(",", ""))

    #return all the data fields collected as a tuple
    return(building, identifier, bed, bath, sqft, formated_rent, 1, formated_date)



def apartment_data(apartment: Apartment):
    URL = apartment.url
    page = requests.get(URL, impersonate="chrome")
    soup = BeautifulSoup(page.content, "lxml")
    
    #get all the url's on the page and select the ones assoicated with details
    urls = [tag['href'] for tag in soup.find_all(class_="more_detail_btn")]
    listing_data = []
    
    #get the data for each listing
    for url in urls:
        item = list_data(url=url, company=apartment.company, building=apartment.building, city=apartment.city)
        print("item")
        print(item)
        if item[0] != "":
            listing_data.append(item)
    #write data from all listings to the csv
    #csv_write(listing_data=listing_data, filename=apartment.filename)
    if listing_data != []:
        db_write(listing_data=listing_data)

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

    for apartment in apartment_list:
        apartment_data(apartment=apartment)


if __name__=="__main__":
    main()
