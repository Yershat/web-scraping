from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from cgitb import text
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
from datetime import datetime
import random

n= random.random()


## Datetime to make csv files that are up to date
now = datetime.now()
date_time = now.strftime("%m.%d.%Y")

headers = {"User-Agent": "UserAgent{}".format(n)}


## City category
print("Enter the city: ")
x = input()
## Last character is removed so suggestions line is present at each case
y = x[0:-1]


## Running Google in headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)


## The starting page
driver.get("https://www.olx.kz/d/rabota/?page={1}")
driver.maximize_window()
time.sleep(3)


## Remove Cookie suggestion
button1 = driver.find_element(By.CLASS_NAME,"css-1ohf0ui")
button1.click()
time.sleep(1)


## Entering the city category
city = driver.find_element(By.CLASS_NAME,"css-kt3c71")
for character in y:
    city.send_keys(character)
    time.sleep(0.3) 
time.sleep(2)


## Clicking the first suggestion and clicking on it 
driver.find_element_by_class_name("css-ngpp9b").click()
time.sleep(2)

## Getting the required attributes from the new page for scraping 
URL = driver.current_url
page = requests.get(URL,headers = headers)
soup = BeautifulSoup(page.content, "html.parser")


## List of all job listings in the current page
list1 = []
mydivs = soup.find_all("a", {"class": "css-1mi714g"})
for i in mydivs:
    list1.append(i.text)


## Function to get number of pages for the given task. Each page is typically 52 listings
list_of_links = driver.find_elements(By.CLASS_NAME,"css-1y8ljz6")
list = []
for i in list_of_links:
    list.append(str(i.text))
x = int(list1[-1])


page = 1

## The loop goes through all the pages and all the job elements inside it
with open('C:/Users/KYershat/Desktop/projects/olx/request_{}.csv'.format(str(date_time)), 'w', encoding='UTF8', newline='') as f:
    fieldnames = ["Job","Company","Name","Phone_number"]
    writer = csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    while page != x+1:
        for i in range(len(list)):
                if driver.find_element_by_xpath("//div[.='" + list[i] + "']").is_displayed():
                    driver.find_element_by_xpath("//div[.='" + list[i] + "']").click()
                    time.sleep(3)
                    url = driver.current_url
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, "html.parser")

                    position = soup.find("div", {"class": "css-mkz7zu"}).get_text(strip=True)

                    m = driver.find_elements_by_xpath("//p[contains(text(), 'Название компании')]") 

                    texts = []

                    for matched_element in m:
                        text = matched_element.text
                        texts.append(text)

                    texts = str(texts)


                    contact_name = soup.find("div", {"class": "css-1fp4ipz"}).get_text(strip=True)
                    contact_name = str(contact_name).partition("Member")[0]

                    time.sleep(1)

                    button2 = driver.find_element(By.CLASS_NAME,"css-cuxnr-BaseStyles")
                    button2.click()
                    time.sleep(3)

                    x = driver.find_elements_by_css_selector("div[class='css-r8u9sk']")
                    phone_number = []
                    for a in x:
                        phone_number.append(a.text)

                    phone_number= str(phone_number)
                    phone_number = phone_number[2:]
                    phone_number = phone_number[:-2]

                    if len(texts) > 0:
                        texts= texts[2:]
                        texts = texts[:-2]

                    elif len(texts) == 0:
                        texts = "None"

                    time.sleep(2)
                    writer.writerow({"Job":position,"Company":texts,"Name":contact_name,"Phone_number":phone_number})
                    time.sleep(2)
                    driver.back()
                    time.sleep(2)
                else:
                    i = i+1
    page = page + 1

