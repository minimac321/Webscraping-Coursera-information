
gui_width = 375
gui_height = 20

# TODO: Make this list dynamic
COURSERA_COURSE_CATEGORY_OPTIONS = [
    "Data Science",
    "Business",
    "Computer Science",
    "Personal Development",
    "Langauge Learning",
    "Information Technology",
    "Health",
    "Math and Logic",
    "Physical Science and Engineering",
    "Social Sciences",
    "Art and Humanities",
]

GOOGLE_SPREADSHEET_NAME = "Coursera_Courses_Server"

GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

CREDENTIALS_JSON = "../coursera-web-scraper-sever.json"
