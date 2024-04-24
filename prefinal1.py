import os
import sys
import time
from datetime import datetime

import pyodbc
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

# Connect to Azure SQL Database
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:sketchdb.database.windows.net,1433;"
    "Database=dreamdb;"
    "Uid=vikasgole;"
    "Pwd=Vikas@123;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

max_retry = 5
retry = 0
try:
    driver.get("https://dreaminterpreter.ai/dream-dictionary")
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div')))

    exit_loop = False
    while not exit_loop:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Dictionary menu
        menu = soup.find('menu', class_='Dictionary_dictionary_menu__mP22l')

        # Find all li tags within the menu
        li_tags = menu.find_all('li')

        # Iterate through the li elements
        count_li_tag = 0
        for li_tag in li_tags[1:]:
            if count_li_tag >= 5:
                break
            if max_retry == 0:
                exit_loop = True
                break

            dict_key = li_tag.text.strip()
            anchor_tag = li_tag.find('a')

            if anchor_tag:
                link = anchor_tag.get('href')

                if link:
                    complete_link = 'https://dreaminterpreter.ai' + link

                    try:
                        driver.get(complete_link)
                        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div')))


                        meaning_page_html = driver.page_source
                        meaning_page_soup = BeautifulSoup(meaning_page_html, 'html.parser')
                        count_li_tag += 1
                        dict_def_div = meaning_page_soup.find('div', class_='Dictionary_definition_container__zX89x')

                        if dict_def_div:
                            heading_tag = dict_def_div.find('h1')
                            if heading_tag:
                                heading_text = heading_tag.text.strip()

                            second_div = dict_def_div.find('div')
                            if second_div:
                                all_content_div = second_div.find_all('div')
                                found_iteration = False
                                count_cont_div = 0
                                for cont_div in all_content_div:
                                    found_iteration = True  # Set to True for each iteration
                                    if count_cont_div >= 5:
                                        break
                                    subheading_anchor = cont_div.find('a')

                                    if subheading_anchor:
                                        subheading = subheading_anchor.find('h3').text.strip()
                                        subheading_word_href = subheading_anchor.get('href')
                                        word_definition_url = 'https://dreaminterpreter.ai' + subheading_word_href

                                        try:
                                            driver.get(word_definition_url)
                                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div')))
                                        except TimeoutException:
                                            print(f"TimeoutException occurred while processing link: {word_definition_url}")
                                            continue

                                        definiton_page_html = driver.page_source
                                        definiton_soup = BeautifulSoup(definiton_page_html, 'html.parser')
                                        word_definition = definiton_soup.find('div', class_='Dictionary_definition_container__zX89x')

                                        if word_definition:
                                            word = word_definition.find('h1').text.strip()
                                            def_paragraph = word_definition.find('p').text.strip()

                                            try:
                                                cursor.execute(
                                                    "INSERT INTO definition_table (char_key, word_definition_url, word, def_paragraph) VALUES (?, ?, ?, ?)",
                                                    (heading_text, word_definition_url, word, def_paragraph)
                                                )
                                                conn.commit()
                                            except pyodbc.IntegrityError as e:
                                                print("Duplicate entry found. Skipping...")
                                                conn.rollback()

                                            all_div = definiton_soup.find_all('div')
                                            related_dream_div = all_div[-8]

                                            if related_dream_div:
                                                dream_heading = related_dream_div.find('ul')

                                                if dream_heading:
                                                    heading_related = dream_heading.find('h1').text.strip()
                                                    dreams_list = dream_heading.find('li')

                                                    if dreams_list:
                                                        dreams_anchor = dreams_list.find('a')

                                                        if dreams_anchor:
                                                            dream_href = 'https://dreaminterpreter.ai' + dreams_anchor.get('href')
                                                            img_title_div = dreams_anchor.find('div', class_='Art_dream_card_container__iLV+l')

                                                            if img_title_div:
                                                                title_div = img_title_div.find('div', class_='Art_dream__NXDhj')

                                                                if title_div:
                                                                    title_text = title_div.text.strip()

                                                            img_tag = img_title_div.find('img')

                                                            if img_tag:
                                                                img_href = img_tag.get('src')

                                                            final_date_div = dreams_anchor.find('div', class_='Art_date__JKl3V').text.strip()

                                                            if final_date_div:
                                                                date_obj = datetime.strptime(final_date_div, '%m/%d/%Y')
                                                                formatted_date = date_obj.strftime('%d/%m/%Y')

                                                            try:
                                                                driver.get(dream_href)
                                                                WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                                                                WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'Interpreter_dream_card_container__NWBLD')))
                                                            except TimeoutException:
                                                                print(f"TimeoutException occurred while processing link: {dream_href}")
                                                                continue

                                                            related_dream_html = driver.page_source
                                                            related_dream_soup = BeautifulSoup(related_dream_html, 'html.parser')
                                                            head_para = related_dream_soup.find('p', class_='Interpreter_dream__Nd9f0').text.strip()
                                                            dream_para = related_dream_soup.find('p', class_='Interpreter_interpretation__B-MVR').text.strip()

                                                            try:
                                                                cursor.execute(
                                                                    "INSERT INTO related_dream (title, formatted_date, img_src, dream_href, head_para, dream_para) VALUES (?, ?, ?, ?, ?, ?)",
                                                                    (title_text, formatted_date, img_href, dream_href, head_para, dream_para)
                                                                )
                                                                conn.commit()
                                                                print("Done")
                                                            except pyodbc.IntegrityError as e:
                                                                print("Duplicate entry found. Skipping...")
                                                                conn.rollback()
                                    if not found_iteration:
                                        break
                                    count_cont_div += 1
                    except TimeoutException:
                        print(f"TimeoutException occurred while processing link: {complete_link}")
                        max_retry -= 1
                        time.sleep(1)
                        continue

except TimeoutException:
    print("TimeoutException occurred")
    print("Reloading....")
    retry += 1
    time.sleep(1)
finally:
    driver.quit()
