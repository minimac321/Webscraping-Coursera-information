import warnings
from typing import Optional

import requests
from bs4 import BeautifulSoup, element

from src.utils import value_to_float


def get_rating_info(html_soup: BeautifulSoup) -> dict:
    """Extract the rating info from a given course card's HTML"""
    overall_ratings_str = html_soup.find_all("span", {"data-test": "number-star-rating"})[0].text
    overall_rating = float(overall_ratings_str.replace("stars", ""))

    ratings_str = html_soup.find_all("span", {"data-test": "ratings-count-without-asterisks"})[
        0
    ].text
    rating = int(ratings_str.split(" ")[0].replace(",", ""))

    rating_info = {
        "rating": rating,
        "overall_rating": overall_rating,
    }

    return rating_info


def get_enrolled_info(html_soup: BeautifulSoup) -> dict:
    """Extract the enrolled number from a given course card's HTML"""
    num_students_enrolled_str = (
        html_soup.find_all("div", {"class": "_1fpiay2"})[0].find("strong").find("span").text
    )
    num_students_enrolled = int(num_students_enrolled_str.replace(",", ""))

    enrolled_info = {
        "num_students_enrolled": num_students_enrolled,
    }

    return enrolled_info


def get_description_info(
    specialized_html_soup: BeautifulSoup, specialized_url: bool = False
) -> dict:
    """Extract the course description from a given course card's HTML"""

    if specialized_url:
        course_description = specialized_html_soup.find_all("div", {"class": "description"})[0].text

    else:
        course_description = (
            specialized_html_soup.find_all("div", {"class": "m-t-1 description"})[0]
            .find("div", {"class": "content-inner"})
            .find("p")
            .text
        )

    description_info = {
        "course_description": course_description,
    }
    return description_info


def get_provider_info(html_soup: BeautifulSoup) -> dict:
    """Extract the course provider from a given course card's HTML"""
    course_provider = html_soup.find_all("h3", {"class": "headline-4-text bold rc-Partner__title"})[
        0
    ].text

    provider_info = {
        "course_provider": course_provider,
    }
    return provider_info


def fetch_course_info_from_course_url(course_url: str):
    """Fetch all course info from a given course card's HTML"""

    if "specializations" == course_url.split("/")[3]:
        specialized_url = True
    else:
        specialized_url = False

    response = requests.get(course_url)
    html_soup = BeautifulSoup(response.content, "html.parser")

    # Get Rating Info
    rating_info = get_rating_info(html_soup)

    # Get Enrolled Info
    enrolled_info = get_enrolled_info(html_soup)

    # Get Provider Info
    provider_info = get_provider_info(html_soup)

    # Get Description Info
    description_info = get_description_info(html_soup, specialized_url)

    # Merge all information into a single dictionary
    merged_dict = {**rating_info, **enrolled_info, **description_info, **provider_info}

    return merged_dict


def get_course_attributes(card: element.ResultSet) -> Optional[dict]:
    """
    Given a single HTML course card from the Coursera website - extract all the necessary
    information

    :return: Dictionary containing the following attributes for a course:
        ['name', 'rating', 'num_of_reviewers', 'url']
    """
    try:
        course_info = {}

        course_name = card.find("h2", {"class": "cds-119 css-bku0rr cds-121"}).text

        course_info["name"] = course_name
        course_info["rating"] = float(card.find("p", {"class": "cds-119 css-zl0kzj cds-121"}).text)
        course_review_data = card.find_all("p", {"class": "cds-119 css-14d8ngk cds-121"})[0].text

        # Set Course Reviews
        course_reviews_str = (
            course_review_data.replace(" reviews", "").replace("(", "").replace(")", "")
        )

        course_num_of_reviewers = value_to_float(course_reviews_str)
        course_info["num_of_reviewers"] = course_num_of_reviewers

        course_info["url"] = card.attrs["href"]
        return course_info

    except Exception as e:
        warnings.warn(f"Exception: {e}")
        return None


def get_all_course_card_info(course_card_soup: BeautifulSoup) -> list[dict]:
    """
    Given a full page of HTML from Coursera - Extract the individual course card information

    :return: A list of dictionaries containing the attributes for individual cards
    """
    course_cards = course_card_soup.find_all(
        "a", {"data-click-key": "search.search.click.search_card"}
    )

    course_information_list = []

    for card in course_cards:
        course_dict = get_course_attributes(card)
        if course_dict is not None:
            course_information_list.append(course_dict)

    return course_information_list
