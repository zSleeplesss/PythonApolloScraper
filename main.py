import csv
import re
import os

from selenium import webdriver
from selenium.common import TimeoutException
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
# Remove service = service if you don't want a headless browser, replace with options = chrome_options
driver = webdriver.Chrome(service=service)
driver.get(next_url)


# Create object for each search query
# I have never done OOP in python so if a lot of this is redundant let me know and I can optimize
class URL:

    def start(self):
        url = self.prefix + str(self.page_index) + self.midfix + self.search_args + self.suffix
        # Go to page
        driver.get(url)

        # Wait until website appears on screen
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "zp_DEEPx"))
        )

        # Make sure arrow element is there before continuing
        # wait.until(EC.element_to_be_clickable(driver.find_element(by=By.CLASS_NAME, value="apollo-icon-chevron-arrow-right")))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_KtrQp")))

        # print("Writing values.")

        # Check if file of same query already exists, delete it if it does
        if self.page_index == 1:
            try:
                os.remove(self.name)
                print(f"{self.name} has been deleted.")
            except FileNotFoundError:
                print(f"{self.name}.csv does not exist. Making one.")
            except PermissionError:
                print(f"Permission denied: unable to delete {self.name}.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            placeholder = 0

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_KtrQp")))
        self.csv_write()

        # Call this recursively to simplify
        if not self.done:
            self.page_index += 1
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "apollo-icon-chevron-arrow-right")))
            next_button = driver.find_element(by=By.CLASS_NAME, value="apollo-icon-chevron-arrow-right")
            next_button.click()
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

        # Load initial page to collect query data
        url = self.prefix + str(self.page_index) + self.midfix + self.search_args + self.suffix
        driver.get(url)

        # Wait to parse page
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "apollo-icon-chevron-arrow-right")))

        # Query num int
        # Also remove commas
        try:
            self.query_num = int(
                re.search(r"of (.+)", driver.find_element(by=By.CLASS_NAME, value="zp_xAPpZ").text).group(1)
            .replace(",", ""))
            # print("query num " + str(self.query_num))
            self.page_num = self.query_num // 25
            # print("page num " + str(self.page_num))
            self.page_remainder = self.query_num % 25
            # print("remainder num " + str(self.page_remainder))

            # Variable to detect when there is only one page
            self.done = False if self.page_num > 0 else True
            self.is_valid = True
        except TimeoutException:
            print("Invalid query: " + self.name + ". Skipping and moving to next query.")
            self.is_valid = False


    def csv_write(self):
        if self.page_index == 1:
            file_write = open(self.name + ".csv", mode="w", newline="")
            writer = csv.writer(file_write)
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
            file_write.close()

        file_append = open(self.name + ".csv", mode="a", newline="")
        appender = csv.writer(file_append)

        self.done = True if self.page_index == self.page_num + 1 else False

        lines = self.page_remainder if self.done else 25

        print("Currently writing lines " + str((self.page_index - 1) * 25) + " through " + str((self.page_index - 1) * 25 + lines))

        for i in range(0, lines):
            # elements.append(str(driver.find_element(By.ID, ("table-row-" + str(i))).text).split("\n"))
            appender.writerow(str(driver.find_element(By.ID, ("table-row-" + str(i))).text).split("\n"))
            # writer.writerows(elements)
        # print(elements)
        file_append.close()


print("If browser window closes and throws an error, just try again. NOTE: Uses Google Chrome.")

# Fetch title of window
title = driver.title
print(title)

# Make reusable webdriver waiter to shorten code length
wait = WebDriverWait(driver, 30)

wait.until(EC.presence_of_element_located((By.NAME, "email")))
wait.until(EC.presence_of_element_located((By.NAME, "password")))
email = driver.find_element(by=By.NAME, value="email")
password = driver.find_element(by=By.NAME, value="password")
# example = wait.until(EC.element_to_be_clickable(driver.find_element(by=By.CLASS_NAME, value="zp_u1f81")))
# print(example.text)

myemail = input("Enter your email: ")
mypassword = input("Enter your password: ")
email.send_keys(myemail)
password.send_keys(mypassword)

form = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "zp_UoIE6")))
# print(driver.find_element(by=By.CLASS_NAME, value="zp_UoIE6").text)
login_wait = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "zp_ZUsLW")))

login_button = driver.find_element(by=By.CLASS_NAME, value="zp_ZUsLW")
login_button.click()
print("Logging in...")

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


# Make array of object constructor parameters
list = []
# Make array for all the objects
batches = []


# Prompt the user for input
current = ""
print("Enter a search query or type \"esc\" to escape: ")
while not current == "esc":
    current = input()
    list.append(current)

# Get rid of escape at end
list.pop(len(list) - 1)
print("Compiling objects...")

# Create objects
for element in list:
    batches.append(URL(driver, element))

print("Starting...")
for batch in batches:
    if batch.is_valid:
        batch.start()