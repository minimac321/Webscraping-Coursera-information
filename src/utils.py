import requests
from bs4 import BeautifulSoup


def get_rating_info(html_soup):
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


def get_enrolled_info(html_soup):
    num_students_enrolled_str = (
        html_soup.find_all("div", {"class": "_1fpiay2"})[0].find("strong").find("span").text
    )
    num_students_enrolled = int(num_students_enrolled_str.replace(",", ""))

    enrolled_info = {
        "num_students_enrolled": num_students_enrolled,
    }

    return enrolled_info


def get_description_info(specialized_html_soup, specialized_url=False):
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


def get_provider_info(html_soup):
    course_provider = html_soup.find_all("h3", {"class": "headline-4-text bold rc-Partner__title"})[
        0
    ].text

    provider_info = {
        "course_provider": course_provider,
    }
    return provider_info


def fetch_course_info_from_course_url(course_url):
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
