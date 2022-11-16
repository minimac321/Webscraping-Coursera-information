
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json

GOOGLE_API_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

SPREADSHEET_NAME = "data_science_course_info"


def test_worksheet(worksheet):
    worksheet_title = worksheet.title
    max_rows = len(worksheet.get_all_values())
    max_cols = len(worksheet.get_all_values()[0])

    print(f"Found sheet {worksheet_title}")


    # first row
    feature_names = worksheet.row_values(1)
    df_courses = pd.DataFrame(columns=feature_names)
    print("df_courses columns", df_courses.columns.tolist())

    for i_row in range(1, max_rows+1):
        row_values = worksheet.row_values(i_row)
        df_courses.loc[len(df_courses)] = row_values

    print(df_courses)


def create_new_worksheet(spreadsheet, worksheet_title, rows=100, cols=20) -> gspread.worksheet.Worksheet:
    new_worksheet = spreadsheet.add_worksheet(title=worksheet_title, index=0,
                                              rows=str(rows), cols=str(cols))
    return new_worksheet


def get_spreadsheet_url(spreadsheet):
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
    return spreadsheet_url


def upload_df(df: pd.DataFrame, worksheet_title: str, spreadsheet):
    # Create new sheet
    new_worksheet = create_new_worksheet(spreadsheet, worksheet_title)
                                         # , rows=len(df)+1, cols=len(df.columns))
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
        "coursera-web-scraper-sever.json", GOOGLE_API_SCOPES
    )
    gspread_factory = gspread.authorize(credentials)
    spreadsheet = gspread_factory.open(SPREADSHEET_NAME)

    spreadsheet_url = get_spreadsheet_url(spreadsheet)

    spreadsheet_dict = {}
    spreadsheet_dict["spreadsheet_url"] = spreadsheet_url

    # Get DF
    coursera_course_df = pd.read_csv(csv_filename, index_col=False)
    worksheet_title = csv_filename.replace(".csv", "")

    new_worksheet = upload_df(coursera_course_df, worksheet_title, spreadsheet)
    worksheet_url = new_worksheet.url
    spreadsheet_dict["worksheet_url"] = worksheet_url

    return spreadsheet_dict
