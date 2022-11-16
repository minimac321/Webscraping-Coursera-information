from gui import create_gui

from src.web_scraper import CourseraWebScraper


def main():
    # window
    web_scraper = CourseraWebScraper()

    tk_window = create_gui(web_scraper)
    tk_window.mainloop()


if __name__ == "__main__":
    main()
