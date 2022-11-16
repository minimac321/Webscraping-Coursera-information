from functools import partial
from tkinter import Label, StringVar, OptionMenu, Button, Tk
import webbrowser

from constants import (
    gui_width,
    gui_height,
    COURSERA_COURSE_CATEGORY_OPTIONS,
    GUI_URL_LABEL_CLICK_HERE_STR,
)


def url_label_click_callback(event):
    """Callback to open URL when label is clicked and processing is complete"""
    web_str = event.widget.cget("text")
    website = web_str.replace(GUI_URL_LABEL_CLICK_HERE_STR, "")

    if len(website) == 0:
        pass
    else:
        webbrowser.open_new(website)


def fetch_coursera_category_info(web_scraper: "CourseraWebScraper", course_category, url_label):
    """
    Fetch all the Coursera data and update the GUI accordingly to display the URL
    """
    web_scraper.logger.info(f"Scraping data from Coursera with category: {course_category.get()}")

    web_scraper.set_course_category(course_category.get())
    worksheet_url = web_scraper.fetch_and_upload_coursera_category_info()

    if worksheet_url is not None:
        # Update Labels
        url_label.configure(text=f"{GUI_URL_LABEL_CLICK_HERE_STR}{worksheet_url}")


def create_gui(web_scraper: "CourseraWebScraper"):
    """
    Create the graphical user interface with the given width and height and initialize all
    components.
    """
    tk_window = Tk()
    tk_window.geometry(f"{gui_width}x{gui_height}")
    tk_window.title("Web Scraping Form")

    # Category Label
    category_label = Label(tk_window, text="Select Coursera Course Category to scrape data from")
    category_label.grid(row=0, column=0, pady=(10, 10), padx=(5, 5))

    # Init Menu Text
    dropdown_menu_text = StringVar()
    dropdown_menu_text.set(COURSERA_COURSE_CATEGORY_OPTIONS[0])

    # Create Dropdown menu
    dropdown_menu = OptionMenu(tk_window, dropdown_menu_text, *COURSERA_COURSE_CATEGORY_OPTIONS)
    dropdown_menu.grid(row=1, column=0, pady=(10, 10), padx=(3, 3))

    url_label = Label(tk_window, text="", fg="blue", cursor="hand2")
    url_label.grid(row=4, column=0, pady=(10, 10), padx=(5, 5))
    url_label.bind("<Button-1>", url_label_click_callback)

    # Create button, it will change label text
    scrap_data = partial(fetch_coursera_category_info, web_scraper, dropdown_menu_text, url_label)

    button = Button(tk_window, text="Click to Scrape Data", command=scrap_data)
    button.grid(row=2, column=0, pady=(10, 10), padx=(3, 3))

    return tk_window
