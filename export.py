import myfitnesspal
import pathlib
from write import *
from datetime import datetime
import json
import pygsheets
import browser_cookie3


def load_config():
    f = open("config.json", "r")
    config = json.load(f)
    f.close()
    return config


config = load_config()

pathToCredentials = pathlib.Path("./credentials.json").absolute()
gc = pygsheets.authorize(service_file=pathToCredentials)

# Find the spreadsheet with the name defined in the config
sh = gc.open(config["SpreadsheetName"])

# Find the index of the sheet with the name defined in the config
sheet_index = get_sheet_index(config["WorksheetName"], sh)
if (sheet_index == -1):
    print("Sheet not found.")
    raise SystemExit

working_sheet = sh[sheet_index]

cookie_jar = None

if config["Browser"] == "Chrome":
    cookie_jar = browser_cookie3.chrome(domain_name="myfitnesspal.com")
elif config["Browser"] == "Firefox":
    cookie_jar = browser_cookie3.firefox(domain_name="myfitnesspal.com")
elif config["Browser"] == "Edge":
    cookie_jar = browser_cookie3.edge(domain_name="myfitnesspal.com")
elif config["Browser"] == "Opera":
    cookie_jar = browser_cookie3.opera(domain_name="myfitnesspal.com")
elif config["Browser"] == "Safari":
    cookie_jar = browser_cookie3.safari(domain_name="myfitnesspal.com")
else:
    print("Browser not supported.")
    raise SystemExit

client = myfitnesspal.Client(cookiejar=cookie_jar)
date_to_get = get_last_written_date_sheet(working_sheet).split(".")
while (date_to_get != -1):
    # Split date string into day, month and year
    date_to_get = get_last_written_date_sheet(working_sheet).split(".")
    print("Getting data for ", date_to_get, "...")
    # check if date is in the future
    print(date_to_get)
    if datetime(int(date_to_get[2]), int(date_to_get[1]), int(date_to_get[0])) > datetime.now():
        print("All dates are written.")
        raise SystemExit

    date = client.get_date(date_to_get[2], date_to_get[1], date_to_get[0])
    # If no data is found for the date, write - - - - to the sheet
    if not date.totals:
        write_data_to_sheet(["-", "-", "-", "-", config["1"]], working_sheet)
        print(
            f"Written - - - - {config['1']} for {date_to_get[0]}.{date_to_get[1]}.{date_to_get[2]}")
    else:
        write_data_to_sheet([date.totals['calories'], date.totals['protein'],
                             date.totals['carbohydrates'], date.totals['fat'], config["5"]], working_sheet)

        print(f"Written {[date.totals['calories'], date.totals['protein'], date.totals['carbohydrates'], date.totals['fat'], {config['5']}]} for {date_to_get[0]}.{date_to_get[1]}.{date_to_get[2]}")

print("All data written to sheet.")
