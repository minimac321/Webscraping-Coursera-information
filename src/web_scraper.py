import os
import urllib
import urllib.parse
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from google_sheets_utils import upload_csv_to_gsheet
from src.constants import RESULT_SECTION_NO_MORE_RESULTS_STR
from src.utils import get_logger
from src.web_scraping_utils import fetch_course_info_from_course_url, get_all_course_card_info


class CourseraWebScraper:
    """
    Web Scraper that searches the Coursera website and extracts all the information for specific
    courses within a courser category.
    """

    base_url = "https://www.coursera.org"

    def __init__(self):
        self.browser = webdriver.Chrome()  # WebDriver
        self.output_worksheet_url = ""
        self.logger = get_logger()

        self.working_dir = "../working_dir/"
        os.makedirs(self.working_dir, exist_ok=True)

        self.course_category = None
        self.courses_df = None
        self.output_csv_name = None

    def fetch_and_upload_coursera_category_info(self) -> Optional[str]:
        """
        Extract high level course information, then add specific course information, save the
        information as a csv locally, then upload the csv to a Google sheet.
        """
        self.extract_high_level_course_category_df()

        if self.courses_df.shape[0] == 0:
            return None

        self.extract_low_level_course_category_information()
        self.write_course_category_data_to_csv()
        output_worksheet_url = self.upload_to_google_sheets()

        return output_worksheet_url

    def fetch_html_from_url(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and return the HTML for given URL if there are results available, otherwise return
        None
        """
        self.browser.get(url)
        html = self.browser.page_source
        course_card_soup = BeautifulSoup(html, "lxml")

        # Check if we have more results
        results_are_finished = (
            course_card_soup.find("div", {"data-e2e": "NumberOfResultsSection"}).text
            == RESULT_SECTION_NO_MORE_RESULTS_STR
        )

        # This works!
        if results_are_finished:
            return None

        return course_card_soup

    def set_course_category(self, course_category: str):
        """Set the course category"""
        self.course_category = course_category

    def get_coursera_page_url_by_page_number(self, page_number: int, entity_type_desc: str) -> str:
        """Generate Coursera URL using page and entity type"""
        url_str = (
            f"{self.base_url}/search?page={page_number}&index=prod_all_launched_products_"
            f"term_optimization&entityTypeDescription={entity_type_desc}"
        )
        topic_url_parsed_str = "&topic=" + urllib.parse.quote(self.course_category.lower())
        full_url = url_str + topic_url_parsed_str
        return full_url

    def extract_low_level_course_category_information(self):
        """
        Extract the course provider and course description on the dedicated course weblink and
        append these attributes to the course dataframe
        """
        for i, row in self.courses_df.iterrows():
            course_name = row["name"]
            course_full_url = self.base_url + row["url"]
            self.logger.info(f"Course: {course_name}. URL: {course_full_url}")

            try:
                merged_dict = fetch_course_info_from_course_url(course_full_url)

                self.courses_df.loc[i, "course_provider"] = merged_dict["course_provider"]
                self.courses_df.loc[i, "course_description"] = merged_dict["course_description"]

            except Exception as e:
                self.logger.info(f"Skipping {course_name} due to Exception {e}")

    def extract_high_level_course_category_df(self, entity_type_desc: str = "Courses"):
        """
        Extract and create a dataframe containing the following columns:
            ['name', 'rating', 'num_of_reviewers', 'url']
        """
        list_of_courses = self.extract_course_category_information(entity_type_desc)

        self.courses_df = pd.DataFrame(list_of_courses)

        self.courses_df["category"] = self.course_category
        self.logger.info(f"Extracted courses df with shape: {self.courses_df.shape}")

    def extract_course_category_information(self, entity_type_desc: str) -> list[dict]:
        """
        Iterate over all the pages for a selected category and entity type and extract all the
        basic course information.
        """
        list_of_courses = []

        for page_number in range(1, 50):
            self.logger.info(f"page_number: {page_number}")
            url = self.get_coursera_page_url_by_page_number(page_number, entity_type_desc)
            self.logger.info(f"url: {url}")

            course_card_soup = self.fetch_html_from_url(url)

            if course_card_soup is None:
                self.logger.info("!!! No more results left !!!")
                break

            course_information_list = get_all_course_card_info(course_card_soup)
            list_of_courses.extend(course_information_list)

        return list_of_courses

    def write_course_category_data_to_csv(self):
        """Save course df to local directory"""
        self.logger.info(f"courses_df shape: {self.courses_df.shape}")
        csv_name = f"{self.course_category.lower().replace(' ', '_')}_course_info.csv"
        self.output_csv_name = os.path.join(self.working_dir, csv_name)
        self.courses_df.to_csv(self.output_csv_name, index=False)

    def upload_to_google_sheets(self) -> str:
        """
        If the csv file was created, upload it into the Google spreadsheet
        """
        if os.path.exists(self.output_csv_name):
            spreadsheet_dict = upload_csv_to_gsheet(self.output_csv_name)
            self.logger.info(f"Worksheet URL: {spreadsheet_dict['worksheet_url']}")

            return spreadsheet_dict["worksheet_url"]
