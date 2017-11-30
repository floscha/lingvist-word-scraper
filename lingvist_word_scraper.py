"""A selenium based web scraper to get all learned words from Lingvist."""
from datetime import datetime
from getpass import getpass
import json
import sys
from time import sleep

from selenium import webdriver


if __name__ == '__main__':
    # Read arguments from command line.
    args = sys.argv[1:]
    if len(args) > 2:
        print("Error: Not more than 2 arguments (email & password) allowed")
        sys.exit(1)

    # Ask user for email or take from arguments.
    if len(args) == 0:
        print("Input email:")
        user_email = input()
    else:
        user_email = args[0]
    # Ask user for password or take from arguments.
    if len(args) < 2:
        print("Input password:")
        user_password = getpass()
    else:
        user_password = args[1]

    # Initialize the Gecko driver for Lingvist.
    driver = webdriver.Firefox(executable_path='geckodriver')
    driver.get("https://learn.lingvist.com")
    print("Start scraping...")
    start_time = datetime.now()

    # 1. Go to login page.
    button = driver.find_element_by_xpath("//button[@data-provider='email']")
    button.click()

    # 2. Login.
    email_input = driver.find_element_by_xpath("//input[@class='email']")
    email_input.send_keys(user_email)
    password_input = driver.find_element_by_xpath("//input[@class='password']")
    password_input.send_keys(user_password)

    login_button = driver.find_element_by_xpath(
        "//button[@class='signin-submit']"
    )
    login_button.click()

    sleep(2)  # Let page load.

    # 3. Go to words page.
    sidebar = driver.find_element_by_xpath("//div[@class='learning-progress']")
    sidebar.click()
    drawer_item = driver.find_element_by_xpath(
        "//div[@class='drawer-item course']"
    )
    drawer_item.click()

    # 4. Scrape words!
    vocabulary = []
    page = 0
    while True:
        page += 1
        word_rows = driver.find_elements_by_xpath("//tr[@class='word-row']")
        for row in word_rows:
            cells = row.find_elements_by_tag_name("td")
            # Word, last practiced and times practiced are a cell each.
            cell_texts = [cell.text for cell in cells]

            # Translation requires click on word.
            word_element = cells[0].find_element_by_xpath("span")
            last_time_correct_raw = word_element.get_attribute("class")
            # class is either 'word correct' or 'word incorrect'.
            last_time_correct_text = last_time_correct_raw.replace('word ', '')
            last_time_correct = (True if last_time_correct_text == 'correct'
                                 else False)
            word_element.click()

            try:
                pre_translation = driver.find_element_by_xpath(
                    "/html/body/div[4]/section/section[2]/table/tbody/tr/td/var"
                ).get_attribute("data-begin")
                translation = driver.find_element_by_xpath(
                    "/html/body/div[4]/section/section[2]/table/tbody/tr[1]/td"
                )
                translation_text = translation.text
                if pre_translation:
                    translation_text = pre_translation + ' ' + translation_text
            except Exception:
                print("Extraction of word '%s' on page %d failed"
                      % (cell_texts[0], page))
                translation_text = None

            vocab = {
                'word': cell_texts[0],
                'translation': translation_text,
                'last_practiced': cell_texts[1],
                'times_practiced': cell_texts[2],
                'last_time_correct': last_time_correct
            }
            vocabulary.append(vocab)

        next_button = driver.find_element_by_xpath(
            "//a[@data-navigation='next']"
        )
        # Stop once the button has class='passive'
        #   which indicates reaching the last page.
        if next_button.get_attribute("class"):
            break

        # Go to next page.
        next_button.click()

    end_time = datetime.now()
    seconds_passed = (end_time - start_time).seconds
    print("Finished scraping after %d seconds" % seconds_passed)
    driver.close()

    with open('vocabulary.json', 'w') as f:
        json.dump(vocabulary, f)
