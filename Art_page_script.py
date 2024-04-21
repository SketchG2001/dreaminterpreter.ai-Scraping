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
driver.get("https://dreaminterpreter.ai/")
driver.minimize_window()
exit_loop = False
while not exit_loop:
    html_content = driver.page_source

    # print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    # html saved to the webpage.html
    # with open("webpage.html", "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())
    #
    # print("html saved to the webpage.htm.")

    # to get all the links
    # for links in soup.find_all('a'):
    #     print(links.get('href'))

    # to get all the anchor tags
    a_tags = soup.find_all('a')
    # Print all <a> tags
    # for a_tag in a_tags:
        # print(a_tag)

    # Get all text of the current page
    # all_text = []
    # for tag in soup.find_all(True):
    #     # print(tag)
    #     tag_text = tag.get_text(strip=True)
    #     if tag_text:
    #         all_text.append(tag_text)
    #
    # print('\n'.join(all_text))
    # loading the Art page
    art_page = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/nav/ul/li[2]/a')
    art_page.click()
    # wait to load the page
    wait = WebDriverWait(driver, 100)
    input_tag = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/input')
    input_tag_value = input_tag.get_attribute('value')

    new_value = "04/21/2024"
    # Clear the input field by sending backspace keystrokes
    input_tag.send_keys(Keys.CONTROL + "a")  # Select all text
    input_tag.send_keys(Keys.BACKSPACE)  # Delete selected text
    input_tag.send_keys(new_value)  # Send the new value
    input_tag.send_keys(Keys.ENTER)

    # Retrieve the updated value
    target_date = input_tag.get_attribute('value')
    # print(target_date)

    specific_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[3]')))
    html_content2 = driver.page_source
    soup2 = BeautifulSoup(html_content2, 'html.parser')

    # find the date input tag

    # print(soup2.prettify())


    # with open("Art.html", "w", encoding="utf-8") as file:
    #     file.write(soup2.prettify())

    li_elements = soup2.find_all('li')
    # it ignores the first 5 li's which is in the navbar
    li_elements_to_process = li_elements[5:]
    # print(li_elements)
    target_date_file_safe = target_date.replace("/", "-")

    with open(f"_{target_date_file_safe}_Art_data.txt", "w", encoding="utf-8") as file:
        with open(f"_{target_date_file_safe}_img_src.txt", "w", encoding="utf-8") as img_file:
            base_url = "https://dreaminterpreter.ai/"
            count = 1
            for li in li_elements_to_process:
                anchor_tag = li.find('a')
                a_href = anchor_tag.get('href')

                if anchor_tag:
                    a_href = anchor_tag.get('href')
                    full_Post_href = base_url + a_href
                    driver.execute_script("document.documentElement.style.setProperty('visibility', 'visible', 'important');")

                    # Navigate to the full Post href
                    driver.get(full_Post_href)
                    wait = WebDriverWait(driver, 50)
                    # Wait for the specific element to be present, indicating that the page has fully loaded
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Interpreter_dream_card_container__NWBLD")))

                    # Now get the page source and print it
                    full_post = driver.page_source
                    full_post_soup = BeautifulSoup(full_post, 'html.parser')


                    all_para_div = full_post_soup.find('div', class_='Interpreter_dream_card_container__NWBLD')
                    if all_para_div:

                        # Find the first paragraph with class 'Interpreter_dream__Nd9f0'
                        first_para = all_para_div.find('p', class_='Interpreter_dream__Nd9f0')
                        if first_para:
                            # print(f"User Input {count}: {first_para.text.strip()}")
                            u_input = f"{count}: {first_para.text.strip()}"
                            # print(u_input)
                        else:
                            print("User input not found.")

                        # Find the second paragraph with class 'Interpreter_interpretation__B-MVR'
                        second_para = all_para_div.find('p', class_='Interpreter_interpretation__B-MVR')
                        if second_para:
                            # print(f"\nInterpreter Response {count}: {second_para.text.strip()}")
                            Response = f"{count}: {second_para.text.strip()}"
                            # print(Response)
                            # print()
                            count += 1
                        else:
                            print("Response not found.")



                    # Wait for document.readyState to be 'complete'
                    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')



                date_elem = li.find('div', class_='Art_date__JKl3V')
                date = date_elem.text.strip() if date_elem else "Date not available"


                title_elem = li.find('div', class_='Art_dream__NXDhj')
                title = title_elem.text.strip() if title_elem else "Title not available"

                img_elem = li.find('img')
                img_src = img_elem['src'] if img_elem else "Image source not available"
                img_file.write(img_src + "\n")

                # Wait for document.readyState to be 'complete'
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

                file.write("Date: {}\n".format(date))
                file.write("\n")
                file.write("Title: {}\n".format(title))
                file.write("\n")
                # file.write("Image Source: {}\n".format(img_src)) # if not required then remove it bcz i have created img url separate file
                # file.write("\n")
                file.write("Full Post: {}\n".format(full_Post_href))
                file.write("\n")
                file.write("User Input: {}\n".format(u_input))
                file.write("\n")
                file.write("Interpreter Response: {}\n".format(Response))
                file.write("\n")
                driver.back()


    user_input = input("Type 'off' to exit: ")
    if user_input.lower() == "off":
        exit_loop = True

driver.quit()