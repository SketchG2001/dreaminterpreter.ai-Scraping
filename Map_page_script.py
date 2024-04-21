import os
import sys

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")  # Enable JavaScript
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://dreaminterpreter.ai/dreamer-map")
# driver.minimize_window()
exit_loop = False
while not exit_loop:

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    # wait to load the regions menu
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/nav')))

    # Extract and print the page source
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
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
    # sys.exit()

    folder_path = "Data_Extracted"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    regions_file = os.path.join(folder_path, "regions.txt")
    if regions:
        region_list = regions.find_all('li')
        with open(regions_file, "w", encoding="utf-8") as country:
            count = 1
            for region in region_list:
                # print(region.text.strip())
                country.write(f'{count}: {region.text.strip()}"\n"')
                count += 1
        print(f'the number of countries are {count-1}')






    user_input = input("Type 'off' to exit: ")
    if user_input.lower() == "off":
        exit_loop = True
driver.quit()
