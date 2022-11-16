import logging

from gui import create_gui
from src.constants import APPLICATION_NAME

from src.web_scraper import CourseraWebScraper


def main():
    logger = logging.getLogger(APPLICATION_NAME)
    logger_handler = logging.StreamHandler()
    logger.addHandler(logger_handler)
    logger.setLevel(logging.INFO)

    # window
    web_scraper = CourseraWebScraper(logger=logger)

    tk_window = create_gui(web_scraper)
    tk_window.mainloop()


if __name__ == "__main__":
    main()
