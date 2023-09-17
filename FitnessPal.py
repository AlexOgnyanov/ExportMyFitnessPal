import myfitnesspal, pathlib
from write import *

# pathToCredentials = pathlib.Path("./credentials.json").absolute()
# gc = pygsheets.authorize(service_file=pathToCredentials)

# sh = gc.open("Alex Ognyanov - PWL")

# sheet_index = get_sheet_index("ДИЕТА", sh)
# if(sheet_index == -1):
#     print("Sheet not found.")
#     raise SystemExit

# working_sheet = sh[sheet_index]

# sheet_data = working_sheet.get_all_values()
# get_last_written_date(sheet_data)

client = myfitnesspal.Client()
date = client.get_date(2023, 9, 14)
