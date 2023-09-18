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
    """
    Returns the index of the sheet with the desired sheetName.

    :param sheetName: str, name of the sheet to find
    :param sh: pygsheets.Spreadsheet, spreadsheet to search in
    """
    for index, i in enumerate(sh):
        if i.title == sheetName:
            return index

    return -1

def get_last_written_row(sheet_data):
    """
    Gets the index of the last written row in the sheet.
    (A column should be a valid date and F column should be empty to be considered as a valid row)
    """
    for index, i in enumerate(sheet_data):
        if is_date(i[0]) and i[5] == "":
            return index
        
    return -1

def get_last_written_row_sheet(working_sheet):
    """
    Same as get_last_written_row, but takes a pygsheets.Worksheet as an argument.
    """
    sheet_data = working_sheet.get_all_values()
    return get_last_written_row(sheet_data)

def get_last_written_date(sheet_data):
    """
    Returns the date of the last written row in the sheet. (Column A)
    """
    return sheet_data[get_last_written_row(sheet_data)][0]

def get_last_written_date_sheet(working_sheet):
    """
    Same as get_last_written_date, but takes a pygsheets.Worksheet as an argument.
    """
    sheet_data = working_sheet.get_all_values()
    return get_last_written_date(sheet_data)

def write_data_to_sheet(data, working_sheet):
    """
    Writes the data to the sheet.
    Data should be in the format [calories, protein, carbohydrates, fat, comment]

    (Works with columns F:J)
    
    :param data: list, data to write to the sheet
    :param working_sheet: pygsheets.Worksheet, sheet to write to
    """
    if(len(data) != 5):
        print("Data not in correct format.")
        raise SystemExit
    
    sheet_data = working_sheet.get_all_values()

    last_written_row = get_last_written_row(sheet_data)
    if(last_written_row == -1):
        print("Last written row not found.")
        raise SystemExit

    working_sheet.update_values(crange=f'F{last_written_row+1}:J{last_written_row+1}', values=[data])