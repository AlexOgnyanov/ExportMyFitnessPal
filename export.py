import myfitnesspal, pathlib
from write import *
from datetime import datetime

pathToCredentials = pathlib.Path("./credentials.json").absolute()
gc = pygsheets.authorize(service_file=pathToCredentials)

sh = gc.open("Alex Ognyanov - PWL")

sheet_index = get_sheet_index("ДИЕТА", sh)
if(sheet_index == -1):
    print("Sheet not found.")
    raise SystemExit

working_sheet = sh[sheet_index]

client = myfitnesspal.Client()
while(get_last_written_date_sheet(working_sheet) != -1):
  date_to_get = get_last_written_date_sheet(working_sheet).split(".")
  if datetime(int(date_to_get[2]), int(date_to_get[1]), int(date_to_get[0])) > datetime.now():
    print("All dates are written.")
    raise SystemExit

  print(date_to_get)
  date = client.get_date(date_to_get[2], date_to_get[1], date_to_get[0])
  print(date.totals)

  if not date.totals:   
    write_data_to_sheet(["-", "-", "-", "-"], working_sheet)
  else:
    write_data_to_sheet([date.totals['calories'], date.totals['protein'], date.totals['carbohydrates'], date.totals['fat']], working_sheet)