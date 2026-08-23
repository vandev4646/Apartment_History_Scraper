# About Apartment History Scraper (vacancyinsights.com)

The goal of this project is to gather listing data from apartment and report on the historical trends.
Currently we are gathering data from each of the apartment buildings for these companies:

- **Regency Property Management Inc**, as of 7/24/26: https://regencypm.com
- **McKenzie Apartment Company**, as of 7/26/26: https://www.mckenzie-apartments.com

Insights gathered are displayed at: https://vacancyinsights.com

## How to contribute

If you would like to see an apartment complex reported on, you can contribute to this repository following the steps below.

1. **Fork** this repo and **clone** it locally
2. Create a **new branch** based off of main and add your scraping script to a file named: **webscraper_companyName.py**. See below for details on what your file must contain.
3. Create a **READ.md** which lists the company name, building name, and URL for each building you are scraping for. This information helps us add the building details to our database.
4. **Commit** your changes and **open a pull request** against the main repository.

**NOTE**: If you would like help getting started, check out this demo on how to scrap a site and contribute to this repo.

### What your .py file must do

The webscraper_mckenzie.py and the webscraper_regeny.py files are great examples of how you can structure your code. These examples utilize BeautifulSoup to scrap the sites but you can use whatever scraping tool you want as long as it outputs data in the correct format.

Your file must collect data in the required format (outlined below) for each apartment unit listed on the webpage. Each of these apartment units tuples must be added to a list. Your code must then pass the list of apartment unit tuples to the db_write funtion, defined in the shared_utilites.py.

**Required Apartment Unit Tuple**
<br>Your list, passed to the db_write function, must contain tuples with the below information, in the below order, for EACH apartment unit listed on the webpage.

- Building (int): You can hardcode one for this. We will update it with the ID from the DB once we add your apartment details(which you outline in the README) to the DB
- Identifier (str) (Address / Unit number if availabe otherwise the desription provided on site)
- Bed (str)
- Bath (str)
- Sq Ft (str)
- Rent Amount (float)
- QTY (int): If your site does not list a quantity of units available, you can hardcode one. This is what we do for the Mckenzie and Regeny examples.

## About the files in this repo

Below is a brief overview of main the files found in this repo.

- **docker-compose.yml, Docker,** and **requirements.txt**: These files are used to run existing code without installing any of the dependencies on your machine. Used by the nightly job on our servers.
- **README.md**: Hello its me ;)
- **shared_utilities.py**: The main function of intrest in this file is db_write. This function takes a listing of apartment data tuples and writes them to our DB.
- **The webscraper_companyName.py** files: Each of these files scraps data from the web and calls the db_write function from the shared_utilities.py file to save the data.
