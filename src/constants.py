APPLICATION_NAME = "Coursera_web_scraper"

gui_width = 800
gui_height = 250

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

AUTH_CREDENTIALS_JSON = "coursera-web-scraper-sever.json"

RESULT_SECTION_NO_MORE_RESULTS_STR = "No results found for your search"


GUI_URL_LABEL_CLICK_HERE_STR = "CLICK HERE FOR LINK\n"
