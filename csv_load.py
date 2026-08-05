import glob
import csv
from datetime import datetime

from shared_utilities import db_write_csv

def main():
    building_mapping = {
    "Blackhawk Trails Apartments": 1,
    "Boulder Creek Apartments": 2,
    "Courtyard Apartments": 3,
    "Highland Ridge Apartments": 4,
    "Homestead Luxury Apartments": 5,
    "Legacy Apartments": 6,
    "Lincoln Street Apartments": 7,
    "Prairie Crest Apartments": 8,
    "Siena Ridge Apartments": 9,
    "The Outlook at 1000 Oaks Apartments": 10,
    "Timber Valley Apartments": 11,
    "Waterside Apartments": 12,
    "Whispering Hills Apartments": 13,
    }
    #get a list of all csv files in the current directory
    csv_files = glob.glob("*.csv")

    for item in csv_files:
        data_list = []
        with open(item, mode="r", encoding="utf-8") as file:
            # Use csv.reader to correctly parse rows
            csv_reader = csv.reader(file)

            # Skip the header row if you do not want it in your final data
            header = next(csv_reader)

            for row in csv_reader:
                building_name = row[1]
                #Replace name with id
                row[1] = building_mapping.get(building_name, building_name)

                rent_clean = row[8].replace("$", "").replace(",", "")
                row[8] = int(rent_clean)

                # 2. Convert Date Logged (Index 11)
                date_obj = datetime.strptime(row[11], "%m_%d_%Y").date()
                row[11] = date_obj

                data_list.append(row)
        db_write_csv(data_list)



if __name__=="__main__":
    main()