import pygsheets
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def get_sheet_index(sheetName, sh):
    #select the first sheet 
    for index, i in enumerate(sh):
        if i.title == sheetName:
            return index

    return -1

def get_last_written_row(sheet_data):
    for index, i in enumerate(sheet_data):
        if is_date(i[0]) and i[5] == "":
            return index
        
    return -1

def get_last_written_date(sheet_data):
    return sheet_data[get_last_written_row(sheet_data)][0]

def get_last_written_date_sheet(working_sheet):
    sheet_data = working_sheet.get_all_values()
    return sheet_data[get_last_written_row(sheet_data)][0]

def write_data_to_sheet(data, working_sheet):
    if(len(data) != 4):
        print("Data not in correct format.")
        raise SystemExit
    
    sheet_data = working_sheet.get_all_values()

    last_written_row = get_last_written_row(sheet_data)
    if(last_written_row == -1):
        print("Last writter row not found.")
        raise SystemExit

    working_sheet.update_values(crange=f'F{last_written_row+1}:I{last_written_row+1}', values=[data])