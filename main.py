import time
import csv
import re
import os

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Install these packages if they're not already on your system btw

CHROMEDRIVER_PATH = './chromedriver'


# url = "https://stackoverflow.com/questions/58773479/beautiful-soup-not-waiting-until-page-is-fully-loaded"
initialurl = "https://app.apollo.io/#/login"
next_url = "https://app.apollo.io/?utm_campaign=Transactional%3A+Account+Activation&utm_content=Transactional%3A+Account+Activation&utm_medium=transactional_message&utm_source=cio#/people?page=1&contactEmailExcludeCatchAll=true&sortAscending=false&sortByField=%5Bnone%5D&qKeywords=bank%20of%20america%20aml&personLocations[]=United%20States"
sext_url = "https://app.apollo.io/?utm_campaign=Transactional%3A+Account+Activation&utm_content=Transactional%3A+Account+Activation&utm_medium=transactional_message&utm_source=cio#/people?page=2&contactEmailExcludeCatchAll=true&sortAscending=false&sortByField=%5Bnone%5D&qKeywords=bank%20of%20america%20aml&personLocations[]=United%20States%22next_url%20%3D%20%22https%3A%2F%2Fapp.apollo.io%2F%3Futm_campaign%3DTransactional%3A%20Account%20Activation&utm_content=Transactional%3A%20Account%20Activation&utm_medium=transactional_message&utm_source=cio"
wext_url = "https://app.apollo.io/?utm_campaign=Transactional%3A+Account+Activation&utm_content=Transactional%3A+Account+Activation&utm_medium=transactional_message&utm_source=cio#/people?qKeywords=bank%20of%20america%20aml&sortByField=%5Bnone%5D&sortAscending=false&page=1"
template_url = "https://app.apollo.io/?utm_campaign=Transactional%3A+Account+Activation&utm_content=Transactional%3A+Account+Activation&utm_medium=transactional_message&utm_source=cio#/people?page=2&qKeywords=bank%20of%20america%20aml&sortByField=%5Bnone%5D&sortAscending=false"

chrome_options = Options()
chrome_options.add_argument("--headless")  # Opens the browser up in background
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
# options = chrome_options
driver = webdriver.Chrome(service=service)
driver.get(next_url)


# Create object for each search query
# I have never done OOP in python so if a lot of this is redundant let me know and I can optimize
class URL:

    def start(self):
        url = self.prefix + str(self.page_index) + self.midfix + self.search_args + self.suffix
        print(url)
        # Go to page
        driver.get(url)

        # Wait until website appears on screen
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "zp_DEEPx"))
        )

        # Make sure arrow element is there before continuing
        # wait.until(EC.element_to_be_clickable(driver.find_element(by=By.CLASS_NAME, value="apollo-icon-chevron-arrow-right")))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_KtrQp")))

        print("Beginning to write values.")

        # Check if file of same query already exists, delete it if it does
        if self.page_index == 1:
            try:
                os.remove(self.name)
                print(f"{self.name} has been deleted.")
            except FileNotFoundError:
                print(f"{self.name} does not exist.")
            except PermissionError:
                print(f"Permission denied: unable to delete {self.name}.")
            except Exception as e:
                print(f"An error occurred: {e}")

        self.csv_write()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "apollo-icon-chevron-arrow-right")))
        next_button = driver.find_element(by=By.CLASS_NAME, value="apollo-icon-chevron-arrow-right")
        next_button.click()

        # Call this recursively to simplify
        if not self.done:
            self.page_index += 1
            self.start()
        else:
            return "Done with object: " + self.search_args

    # Object constructor
    # I was going to use overloading, but python apparently doesn't support it which is SUPER lame
    def __init__(self, driver, search_args,
                 prefix="https://app.apollo.io/?utm_campaign=Transactional%3A+Account+Activation&utm_content=Transactional%3A+Account+Activation&utm_medium=transactional_message&utm_source=cio#/people?page=",
                 page_index=1, midfix="&qKeywords=",
                 suffix="&sortByField=%5Bnone%5D&sortAscending=false&personLocations[]=United%20States"):
        # "https://app.apollo.io/?utm_campaign=Transactional%3A+Account+Activation&utm_content=Transactional%3A+Account+Activation&utm_medium=transactional_message&utm_source=cio#/people?page=2&qKeywords=bank%20of%20america%20aml&sortByField=%5Bnone%5D&sortAscending=false&personLocations[]=United%20States"

        # Initialize all values
        self.prefix = prefix
        self.page_index = page_index
        self.midfix = midfix
        self.suffix = suffix

        # Set csv filename before changing args
        self.name = search_args
        # I was gonna write a loop above but python makes this easy to modify spaces to work in URL arguments
        self.search_args = search_args.replace(" ", "%20")
        # self.search_args = self.parse_args(self, search_args)

        self.query_num = int(
            re.search(r"of (.+)", driver.find_element(by=By.CLASS_NAME, value="zp_xAPpZ").text).group(1))
        print(self.query_num)
        self.page_num = self.query_num // 25
        self.page_remainder = self.query_num % 25

        # Variable to detect when there is only one page
        self.done = False if self.page_num > 0 else True

    def csv_write(self):
        # if ()
        file_write = open(self.name + ".csv", mode="w", newline="")
        file_append = open(self.name + ".csv", mode="a", newline="")

        writer = csv.writer(file_write)
        appender = csv.writer(file_append)

        self.done = True if page_index == page_num else False
        if self.page_index == 1:
            writer.writerow([

                "Name",

                "Job title",

                "Company",
                "Emails",

                "Phone numbers",

                "Actions",

                "Links",

                "Location",

                "Company · Number of employees",

                "Company · Industries",

                "Company · Keywords"])

        # elements = []
        lines = self.page_remainder if self.done else 25

        for i in range(0, lines):
            # elements.append(str(driver.find_element(By.ID, ("table-row-" + str(i))).text).split("\n"))
            appender.writerow(str(driver.find_element(By.ID, ("table-row-" + str(i))).text).split("\n"))
            # writer.writerows(elements)
        # print(elements)
        file_write.close()
        file_append.close()


print("If browser window closes and throws an error, just try again. NOTE: Uses Google Chrome.")

# Fetch title of window
title = driver.title
print(title)

# Make reusable webdriver waiter to shorten code length
wait = WebDriverWait(driver, 30)

emailwait = wait.until(EC.element_to_be_clickable(driver.find_element(by=By.NAME, value="email")))
passwordwait = wait.until(EC.element_to_be_clickable(driver.find_element(by=By.NAME, value="password")))
email = driver.find_element(by=By.NAME, value="email")
password = driver.find_element(by=By.NAME, value="password")
example = wait.until(EC.element_to_be_clickable(driver.find_element(by=By.CLASS_NAME, value="zp_u1f81")))
print(example.text)

myemail = input("Enter your email: ")
mypassword = input("Enter your password: ")
email.send_keys(myemail)
password.send_keys(mypassword)

form = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_UoIE6")))
print(driver.find_element(by=By.CLASS_NAME, value="zp_UoIE6").text)
login_wait = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "zp_ZUsLW")))

login_button = driver.find_element(by=By.CLASS_NAME, value="zp_ZUsLW")
login_button.click()
print("LOGIN BUTTON CLICKED")

cookies = driver.get_cookies()

driver.get(next_url)

# check = wait.until(EC.element_to_be_clickable(driver.find_element(by=By.CLASS_NAME, value="zp_KtrQp")))

wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "zp_DEEPx"))
)
print("Login successful.")
# soup = BeautifulSoup(driver.page_source, "html.parser")
# print(soup.prettify())

# Now need to wait until table elements are visible
tablewait = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_KtrQp")))
# TABLE ROWS in format id = table-row-0
# CELL is class = zp_KtrQp

# BofA = URL(driver, "bank of america aml")
#
# BofA.start()

# Make array for all the objects
batches = []
# Prompt the user for input
print("Enter a search query or type \"esc\" to escape: ")
while not input() == "esc":
    current = input()
    batches.append(URL(driver, current))

for batch in batches:
    batch.start()
