from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime, time as tm, os, glob, shutil, subprocess
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



# BEGIN SCRAPPING
service = Service(ChromeDriverManager().install())
options = Options()
#options.add_argument("--headless")

#Search in google chrome
driver = webdriver.Chrome(service=service, options=options)
name = "pita lite military trail"
driver.get(name + " reviews")
driver.implicitly_wait(10)
#get the review count
review_count = driver.find_element(By.CSS_SELECTOR,
    "span.hqzQac span[data-ved] a span[data-ved]"
).text

print(review_count)

driver.quit()