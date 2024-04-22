import os
import sys
import time

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
    count = 0
    for li_tag in li_elements_to_process:
        # print(li_tag.text.strip())
        dict_key = li_tag.text.strip()
        # sys.exit()
        anchor_tag = li_tag.find('a')
        if anchor_tag:
            link = anchor_tag.get('href')
            # print("link is: ",link)
            if link:
                complete_link = 'https://dreaminterpreter.ai' + link
                # print(complete_link)
                max_attempts = 5  # Maximum number of retry attempts
                attempts = 0
                while attempts < max_attempts:
                    try:

                        # with open("Data_Extracted/dictionary_data/dictionary_key_urls.txt", "a",encoding='utf-8') as key_urls:
                        #     key_urls.write(f"{dict_key}: {complete_link}\n")

                        driver.get(complete_link)
                        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div')))
                        meaning_page_html = driver.page_source
                        meaning_page_soup = BeautifulSoup(meaning_page_html, 'html.parser')
                        # print(meaning_page_soup.prettify())
                        # with open(f"HTML _Extracted/dictionary_HTML/{dict_key}_key.html", 'a', encoding='utf-8') as file:
                        #     file.write(meaning_page_soup.prettify())
                        count += 1
                        dict_def_div = meaning_page_soup.find('div',class_='Dictionary_definition_container__zX89x')
                        # print(dict_def_div)
                        with open("output_file.txt", "a", encoding='utf-8') as output_file:
                            with open("hrefs_file.txt", "a", encoding='utf-8') as hrefs_file:
                                if dict_def_div:
                                    heading_tag = dict_def_div.find('h1')
                                    if heading_tag:
                                        heading_text = heading_tag.text.strip()
                                        output_file.write(heading_text + "\n")
                                    second_div = dict_def_div.find('div')
                                    if second_div:
                                        all_content_div = second_div.find_all('div')
                                        if all_content_div:
                                            for content_div in all_content_div:
                                                subheading_anchor = content_div.find('a')
                                                if subheading_anchor:
                                                    # on the dictionary page as per passed key
                                                    subheading = subheading_anchor.find('h3').text.strip()
                                                    # https: // dreaminterpreter.ai / dream - dictionary / a
                                                    subheading_href = subheading_anchor.get('href')
                                                    output_file.write(subheading + "\n")
                                                    hrefs_file.write(f'{count}: https://dreaminterpreter.ai{subheading_href}' + "\n")
                                                paragraph = content_div.find('p').text.strip()
                                                output_file.write(paragraph + "\n")

                        # if count == 1:
                        #     break



                        break
                    except TimeoutException:
                        print(f"TimeoutException occurred while processing link: {complete_link}")
                        attempts += 1
                        time.sleep(1)
                else:
                    print(f"Maximum retry attempts reached for link: {complete_link}. Moving to the next link.")
            # if count == 1:
            #     break












    user_input = input("Type 'off' to exit: ")
    if user_input.lower() == "off":
        exit_loop = True
driver.quit()




