# Coursera Course Information Webscraper

### Project Brief: 
Create a webscraper to automatically scan all the Coursera website for a specific course category. Then extract the following details about the course:
- Course name
- Course provider 
- Course description
- \# of Students enrolled
- \# of Ratings 

Then upload the results to a Google spreadsheet.

<br>

##### This project uses the following technologies:
- Selenium, requests, and beautifulsoup4 as the web scraping engine and HTML parsers.
- google-api-python-client and gspread for connecting and using a Spreadsheet like a server for 
- uploading.
- pandas and numpy for data manipulation.
- Tkinter to create the graphical user interface 


## Getting started

#### 0. Project Setup
Create virtual environment (There are many other ways to do this). The activate it
```commandline
pyenv virtualenv 3.9.5 coursera-web-scraper-3.9.5
```

Install Dependencies
```commandline
pip install requirements.txt
```

Add Flask Variables
```commandline
export FLASK_APP=main
```

#### 1. Follow tutorial on how to Enable Google Sheets and Google Drive API


Follow the 'Google Setup' part of [this](https://www.makeuseof.com/tag/read-write-google-sheets-python) 
tutorial. Once completed you should have a JSON file which contains your Google Authentication
information. Ensure this file is in the root directory and is named "coursera-web-scraper-sever.json".


**To run the application**
```commandline
flask run
```

Open the application by visiting `http://127.0.0.1:5000` in your browser

Once the application has started select a Courser Category from which to scrape data from. 

Once the data has been scraped it will be uploaded to a Google Sheet and the URL for that sheet will
be shown on the browser.
