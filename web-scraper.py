import urllib
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup, element

import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from gui import create_gui
from utils import fetch_course_info_from_course_url


def value_to_float(value) -> float:
    """
    Convert a value which may be a string, float or int to a float.
    """
    if type(value) == float or type(value) == int:
        return value

    value = value.replace(",", ".").upper()
    if 'K' in value:
        if len(value) > 1:
            return float(value.replace('K', '')) * 1000
        return 1000.0
    if 'M' in value:
        if len(value) > 1:
            return float(value.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in value:
        return float(value.replace('B', '')) * 1000000000

    return 0.0


def get_course_attributes(card: element.ResultSet) -> dict:
    """
    Given a single HTML course card from the Coursera website - extract all the neccessary
    information

    :return: Dictionary containing the following attributes for a course:
        [name, rating, num_of_reviewers, url]
    """
    course_info = {}

    course_name = card.find("h2", {"class": "cds-119 css-bku0rr cds-121"}).text

    course_info["name"] = course_name
    course_info["rating"] = float(card.find("p", {"class": "cds-119 css-zl0kzj cds-121"}).text)
    course_review_data = card.find_all("p", {"class": "cds-119 css-14d8ngk cds-121"})[0].text

    # Set Course Reviews
    course_reviews_str = course_review_data.replace(" reviews", "").replace("(", "").replace(")", "")

    course_num_of_reviewers = value_to_float(course_reviews_str)
    course_info["num_of_reviewers"] = course_num_of_reviewers

    course_info["url"] = card.attrs["href"]

    return course_info


def get_all_course_card_info(course_card_soup: BeautifulSoup) -> list[dict]:
    """
    Given a full page of HTML from Coursera - Extract the individual course card information

    :return: A list of dictionaries containing the attributes for individual cards
    """
    # course_cards = course_card_soup.find_all("div", {"class": "css-ilhc4l"})
    course_cards = course_card_soup.find_all("a",
                                             {"data-click-key": "search.search.click.search_card"})

    course_information_list = []

    for card in course_cards:
        course_dict = get_course_attributes(card)
        course_information_list.append(course_dict)

    return course_information_list


class CourseraWebScraper:

    base_url = "https://www.coursera.org"

    def __init__(self):
        self.browser = webdriver.Chrome()  # WebDriver
        self.course_category = None
        self.courses_df = None

    def fetch_html_from_url(self, url: str) -> Optional[BeautifulSoup]:
        self.browser.get(url)
        html = self.browser.page_source
        course_card_soup = BeautifulSoup(html, 'lxml')

        # Check if we have more results
        results_are_finished = course_card_soup.find("div", {
            "data-e2e": "NumberOfResultsSection"}).text == "No results found for your search"

        # This works!
        if results_are_finished:
            return None

        return course_card_soup

    def set_course_category(self, course_category: str):
        """ Set the course category """
        self.course_category = course_category

    def get_coursera_page_url_by_page_number(self, page_number: int, entity_type_desc: str) -> str:
        """
        Generate Coursera URL using page and entity type
        """
        url_str = f"{self.base_url}/search?page={page_number}&index=prod_all_launched_products_term_optimization&entityTypeDescription={entity_type_desc}"
        topic_url_parsed_str = "&topic=" + urllib.parse.quote(self.course_category)
        full_url = url_str + topic_url_parsed_str
        return full_url

    def extract_low_level_course_category_df(self, entity_type_desc="Courses"):
        for i, row in self.courses_df.iterrows():
            course_name = row["name"]
            course_full_url = self.base_url + row["url"]
            print(f"Course: {course_name}. URL: {course_full_url}")

            merged_dict = fetch_course_info_from_course_url(course_full_url)
            print("merged_dict", merged_dict)

            self.courses_df.loc[i, "course_provider"] = merged_dict["course_provider"]
            self.courses_df.loc[i, "course_description"] = merged_dict["course_description"]

    def extract_high_level_course_category_df(self, entity_type_desc: str ="Courses"):
        list_of_courses = self.extract_course_category_information(entity_type_desc)

        self.courses_df = pd.DataFrame(list_of_courses)
        self.courses_df["category"] = self.course_category
        print(f"Extracted courses_df with shape: {self.courses_df.shape}")

    def extract_course_category_information(self, entity_type_desc: str) -> list[dict]:
        list_of_courses = []

        for page_number in range(1, 3):
            print(f"page_number: {page_number}")
            url = self.get_coursera_page_url_by_page_number(page_number, entity_type_desc)
            print("url", url)

            course_card_soup = self.fetch_html_from_url(url)

            if course_card_soup is None:
                print("!!! No  all courses !!!")
                break

            course_information_list = get_all_course_card_info(course_card_soup)
            list_of_courses.extend(course_information_list)

        return list_of_courses

    def write_category_data_to_csv(self):
        print(self.courses_df.head())
        output_file_name = f"{self.course_category.lower().replace(' ', '-')}_course_info.csv"
        self.courses_df.to_csv(output_file_name, index=False)


def main():
    # window
    web_scraper = CourseraWebScraper()

    tk_window = create_gui(web_scraper)
    tk_window.mainloop()


if __name__ == "__main__":
    main()

    # from pydrive.auth import GoogleAuth
    #
    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()  #