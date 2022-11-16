from functools import partial
from tkinter import Label, StringVar, OptionMenu, Button, Tk

from constants import gui_width, gui_height, COURSERA_COURSE_CATEGORY_OPTIONS


def fetch_coursera_category_info(web_scraper, course_category):
    print(f"Scraping data from Coursera with category: {course_category.get()}")

    web_scraper.set_course_category(course_category.get())
    web_scraper.fetch_and_upload_coursera_category_info()


def create_gui(web_scraper):
    tk_window = Tk()
    tk_window.geometry(f'{gui_width}x{gui_height}')
    tk_window.title('Web Scraping Form')

    # username label and text entry box
    category_label = Label(tk_window, text="Select Coursera Course Category to scrape data from")
    category_label.grid(row=0, column=0, pady=(10, 10), padx=(5, 5))

    # Init Menu Text
    dropdown_menu_text = StringVar()
    dropdown_menu_text.set(COURSERA_COURSE_CATEGORY_OPTIONS[0])

    # Create Dropdown menu
    dropdown_menu = OptionMenu(
        tk_window, dropdown_menu_text, *COURSERA_COURSE_CATEGORY_OPTIONS
    )
    dropdown_menu.grid(row=1, column=0, pady=(10, 10), padx=(3, 3))

    # Create button, it will change label text
    scrap_data = partial(fetch_coursera_category_info, web_scraper, dropdown_menu_text)

    button = Button(tk_window, text="Click to Scrape Data", command=scrap_data)
    button.grid(row=2, column=0, pady=(10, 10), padx=(3, 3))

    return tk_window
