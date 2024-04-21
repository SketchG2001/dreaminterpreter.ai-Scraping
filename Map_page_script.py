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
driver.get("https://dreaminterpreter.ai/dreamer-map")
# driver.minimize_window()
exit_loop = False
while not exit_loop:

    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    # wait to load the regions menu
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/nav')))

    # Extract and print the page source
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    # uncoment the code as per the requirement
    # print(soup.prettify())
    # Specify the file path within the folder
    # folder_path = "HTML _Extracted"
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
    # file_path = os.path.join(folder_path, "Map_page.html")
    #
    # writing the html to the file and saving
    # with open(file_path, "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())

    regions = soup.find('menu', class_='Dictionary_dictionary_menu__mP22l')
    # print(regions.prettify())

    folder_path = "Data_Extracted"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    regions_file = os.path.join(folder_path, "regions.txt")
    if regions:
        region_list = regions.find_all('li')
        with open(regions_file, "w", encoding="utf-8") as country:
            count = 1
            for li_tag in region_list:
                anchor_tag = li_tag.find('a')
                if anchor_tag:
                    country_name = anchor_tag.text.strip()

                    href = anchor_tag.get('href')
                    complete_url = f'https://dreaminterpreter.ai/{href}'
                    # print(complete_url)
                    country.write(f'{count}: {li_tag.text.strip()} - {complete_url}\n')
                    count += 1
                    region_page = driver.get(complete_url)

                    try:
                        wait = WebDriverWait(driver, 15)
                        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                        # wait to load the regions menu
                        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]')))
                        ul_element  = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="art_gallery"]')))
                        if ul_element:
                            list_items = ul_element.find_elements(By.TAG_NAME, 'li')
                            post_count = 1
                            for i, li in enumerate(list_items, start=1):

                                a_tag = li.find_element(By.TAG_NAME, 'a')
                                date = a_tag.find_element(By.CLASS_NAME, 'Art_date__JKl3V').text
                                title = a_tag.find_element(By.CLASS_NAME, 'Art_dream__NXDhj').text.strip()
                                href = a_tag.get_attribute('href').strip()
                                img_tag = a_tag.find_element(By.TAG_NAME,'img')
                                img_src = img_tag.get_attribute('src').strip()
                                img_alt = img_tag.get_attribute('alt').strip()


                                with open(f"Data_Extracted/countries_post_list.txt", "a", encoding="utf-8") as data_file:

                                    data_file.write(f'{post_count}-{i}: {country_name}\n')
                                    data_file.write(f'Date: {date}\n')
                                    data_file.write(f'Title: {title}\n')
                                    data_file.write(f'Post URL: {href}\n')
                                    data_file.write(f'Image URL: {img_src}\n')
                                    data_file.write('\n')
                                post_count += 1

                    except TimeoutException:
                        print(f"Element not found on page: {complete_url}")
                        with open("Data_Extracted/no_data.txt", "a", encoding="utf-8") as no_data_file:
                            no_data_file.write(f"Country: {country_name}, URL: {complete_url}\n")
                        continue

                    region_page_html = driver.page_source
                    region_soup = BeautifulSoup(region_page_html, 'html.parser')
                    country_page = region_soup.prettify()
                    # with open(f"{country_name}.html", "w", encoding="utf-8") as country_file:
                    #     country_file.write(country_page)

                # if count == 15:
                #     break
            print(f'the number of countries are {count - 1}')

    user_input = input("Type 'off' to exit: ")
    if user_input.lower() == "off":
        exit_loop = True
driver.quit()
