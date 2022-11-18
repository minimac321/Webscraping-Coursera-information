from flask import Flask, render_template, jsonify, request

from src.constants import APPLICATION_NAME, COURSERA_COURSE_CATEGORY_OPTIONS
from src.web_scraper import CourseraWebScraper

app = Flask(APPLICATION_NAME, template_folder='templates')


@app.route('/')
def index():
    return render_template(
        'index.html',
        courser_options_list=COURSERA_COURSE_CATEGORY_OPTIONS,
    )


@app.route('/scrape_data/', methods=['POST'])
def fetch_data():
    course_category = request.args.get('course_category')

    web_scraper = CourseraWebScraper(num_pages_to_scrape=3)
    web_scraper.set_course_category(course_category)
    worksheet_url = web_scraper.fetch_and_upload_coursera_category_info()

    if worksheet_url is None:
        text = "None. Issue with Coursera.org - Try again in a few minutes"
        return {'worksheet_url': text}

    data = {'worksheet_url': worksheet_url}
    data = jsonify(data)
    return data
