# Lingvist Word Scraper

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ebe329d47dc547079038e86f28fe8734)](https://www.codacy.com/app/floscha/lingvist-word-scraper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=floscha/lingvist-word-scraper&amp;utm_campaign=Badge_Grade)

Extracts and saves all words a user has learned on Lingvist, including the following additional information:
- The word's translation
- When it was last practiced
- How many times it was practiced in total
- Whether or not the user was correct when he/she last practiced the word


## Disclaimer
This code is mainly for learning purposes to illustrate how data can be scraped from a dynamic web application that requires a user to log in.

Please be aware that according to section (3) of the [Lingvist Terms of Service](https://lingvist.com/tos/), scraping data from their service is not allowed and using this script will happen at your own responsibility!


## Usage

1. Make sure Python (including pip) is installed.

2. Install [Selenium](http://selenium-python.readthedocs.io/) if it is not already installed:
```
$ pip install selenium
```

3. Download the [geckodriver](https://github.com/mozilla/geckodriver) executable (e.g. from [here](https://github.com/mozilla/geckodriver/releases)) and place it in the project folder.

4. Run the script from the project folder using:
```
$ python lingvist_word_scraper.py
```
and enter your email address as well as the password for your account.
Alternatively, you can also pass just your email address or both email and password as command line arguments to the script.
The program will then run to retrieve your words.

5. When the program is finished, you can find all your learned words in the _vocabulary.json_ file.
