import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from constants import GOOGLE_API_SCOPES, GOOGLE_SPREADSHEET_NAME, CREDENTIALS_JSON


def create_new_worksheet(
    spreadsheet, worksheet_title, rows=100, cols=20
) -> gspread.worksheet.Worksheet:
    """
    If worksheet exists then clear it, otherwise create a new sheet
    """
    # Check if it exists
    worksheet_titles = [w.title for w in spreadsheet.worksheets()]

    if worksheet_title in worksheet_titles:
        # get sheet and clear it
        worksheet = spreadsheet.worksheet(title=worksheet_title)
        worksheet.clear()
    else:
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_title, index=0, rows=str(rows), cols=str(cols)
        )
    return worksheet


def get_spreadsheet_url(spreadsheet):
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
    return spreadsheet_url


def upload_df(df: pd.DataFrame, spreadsheet, worksheet_title: str):
    # Create new sheet
    new_worksheet = create_new_worksheet(spreadsheet, worksheet_title)

    # Add columns names
    column_names = df.columns.tolist()
    new_worksheet.insert_row(column_names, 1)

    # Then add all data
    list_of_tuple_to_append = df.to_records(index=False)
    list_of_rows_to_append = [list(r) for r in list_of_tuple_to_append]
    new_worksheet.append_rows(values=list_of_rows_to_append)

    return new_worksheet


def upload_csv_to_gsheet(csv_filename):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_JSON, GOOGLE_API_SCOPES
    )
    gspread_factory = gspread.authorize(credentials)
    spreadsheet = gspread_factory.open(GOOGLE_SPREADSHEET_NAME)

    spreadsheet_url = get_spreadsheet_url(spreadsheet)

    spreadsheet_dict = {}
    spreadsheet_dict["spreadsheet_url"] = spreadsheet_url

    # Get DF
    coursera_course_df = pd.read_csv(csv_filename, index_col=False)
    worksheet_title = csv_filename.replace(".csv", "")

    new_worksheet = upload_df(coursera_course_df, spreadsheet, worksheet_title)
    worksheet_url = new_worksheet.url
    spreadsheet_dict["worksheet_url"] = worksheet_url

    return spreadsheet_dict
