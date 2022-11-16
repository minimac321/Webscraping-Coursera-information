# Webscraping-Coursera-information


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

#### 1. Follow tutorial on how to Enable Google Sheets and Google Drive API


Follow the 'Google Setup' part of [this](https://www.makeuseof.com/tag/read-write-google-sheets-python) 
tutorial. Once completed you should have a JSON file which contains your Google Authentication
information. Ensure this file is in the root directory and is named "coursera-web-scraper-sever.json".


**To run the application**
```commandline
python src/main_application.py
```

Once the application has started select the Graphical User Interface will allow you to select a 
Courser Category from which to scrape data from. 

Once the data has been scraped it will be uploaded to a Google Sheet and the URL for that sheet will
be shown on the interface.
