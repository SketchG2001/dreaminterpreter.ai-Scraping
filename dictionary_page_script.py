import os
import sys

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")  # Enable JavaScript
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
# driver.maximize_window()
driver.get("https://dreaminterpreter.ai/dream-dictionary")
# driver.minimize_window()
exit_loop = False
while not exit_loop:
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    # wait to load the regions menu
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div')))
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())
    #  saving html of dictionary page to the  file
    # with open("HTML _Extracted/DreamDictionary.html", "w") as file:
        # file.write(soup.prettify())

    # Dictionary menue
    menu = soup.find('menu', class_='Dictionary_dictionary_menu__mP22l')

    # Find all li tags within the menu
    li_tags = menu.find_all('li')

    # Print the text content of each li tag
    # li tags to be ignored
    li_elements_to_process = li_tags[1:]
    for li_tag in li_elements_to_process:
        # print(li_tag.text.strip())
        anchor_tag = li_tag.find('a')
        if anchor_tag:
            link = anchor_tag.get('href')
            if link:
                complete_link = 'https://dreaminterpreter.ai' + link
                # print(complete_link)
                driver.get(complete_link)
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div')))
                meaning_page_html = driver.page_source
                meaning_page_soup = BeautifulSoup(meaning_page_html, 'html.parser')
                print(meaning_page_soup.prettify())
                sys.exit()










    user_input = input("Type 'off' to exit: ")
    if user_input.lower() == "off":
        exit_loop = True
driver.quit()