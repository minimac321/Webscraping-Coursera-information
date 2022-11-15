from functools import partial
from tkinter import Label, StringVar, OptionMenu, Button, Tk


def fetch_coursera_category_info(web_scraper, course_category):
    print(f"Scraping data from Coursera with category {course_category.get()}")

    web_scraper.fetch_info()
    return


def create_gui(web_scraper):
    tkWindow = Tk()
    tkWindow.geometry('375x200')
    tkWindow.title('Tkinter Login Form')

    # username label and text entry box
    category_label = Label(tkWindow, text="Select Coursera Course Category to scrape data from"). \
        grid(row=0, column=0, pady=(10, 10), padx=(5, 5))
    username = StringVar()

    # Dropdown menu options
    # TODO: Fetch Automatically
    options = [
        "Data Science",
        "Business",
    ]

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set(options[0])

    # Create Dropdown menu
    drop = OptionMenu(tkWindow, clicked, *options). \
        grid(row=1, column=0, pady=(10, 10), padx=(3, 3))

    # Create button, it will change label text
    scrap_data = partial(fetch_coursera_category_info, web_scraper, clicked)

    button = Button(tkWindow, text="Click to Scrape Data", command=scrap_data). \
        grid(row=2, column=0, pady=(10, 10), padx=(3, 3))

    return tkWindow
