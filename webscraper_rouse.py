from curl_cffi import requests
from bs4 import BeautifulSoup

URL = "https://rousecommunity.com/listings/the-sovereign/"

page = requests.get(URL, impersonate="chrome")

soup = BeautifulSoup(page.content, 'lxml')

table_rows = soup.find("tbody").find_all("tr")
bed = table_rows[0].find('td', {'data-label': 'Size'}).get_text(strip=True)
bed_clean = bed.split()[0]
identifier = table_rows[0].find('td', {'data-label': 'Style'}).get_text(strip=True)
sqft = table_rows[0].find('td', {'data-label': 'Sq Ft'}).get_text(strip=True)
rent = table_rows[0].find('td', {'data-label': 'Price'}).get_text(strip=True)
clean_rent = float(rent.replace("$", "").replace(",", ""))
