from functools import partial
from tkinter import Label, StringVar, OptionMenu, Button, Tk

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


def fetch_coursera_category_info(web_scraper, course_category):
    print(f"Scraping data from Coursera with category {course_category.get()}")

    web_scraper.set_course_category(course_category.get())
    web_scraper.extract_high_level_course_category_df()
    web_scraper.extract_low_level_course_category_df()
    web_scraper.write_category_data_to_csv()

    return


def create_gui(web_scraper):
    tk_window = Tk()
    tk_window.geometry('375x200')
    tk_window.title('Tkinter Login Form')

    # username label and text entry box
    category_label = Label(tk_window, text="Select Coursera Course Category to scrape data from")
    category_label.grid(row=0, column=0, pady=(10, 10), padx=(5, 5))

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set(COURSERA_COURSE_CATEGORY_OPTIONS[0])

    # Create Dropdown menu
    drop = OptionMenu(
        tk_window, clicked, *COURSERA_COURSE_CATEGORY_OPTIONS
    )
    drop.grid(row=1, column=0, pady=(10, 10), padx=(3, 3))

    # Create button, it will change label text
    scrap_data = partial(fetch_coursera_category_info, web_scraper, clicked)

    button = Button(tk_window, text="Click to Scrape Data", command=scrap_data)
    button.grid(row=2, column=0, pady=(10, 10), padx=(3, 3))

    return tk_window
