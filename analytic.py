from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time as tm

def removeNonDigit(text):
    for char in text:
        if not char in "0123456789":
            text = text.replace(char,'')
    return text.strip()


# BEGIN SCRAPPING
service = Service(ChromeDriverManager().install())
options = Options()
#options.add_argument("--headless")

#Search in google chrome
driver = webdriver.Chrome(service=service, options=options)
name = ""
# open the google search page
driver.get("https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwi39uKNi5eJAxUcnYkEHUoYJPYQPAgI")
wait = WebDriverWait(driver,10)
tm.sleep(5)
search_bar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".gLFyf")))
search_bar.send_keys(name + " reviews")
search_bar.send_keys(Keys.RETURN)
tm.sleep(5)
#get the review count
review_count_string = driver.find_element(By.CSS_SELECTOR, ".hqzQac span a span").text
review_count = int(removeNonDigit(review_count_string))

print(f"{review_count} is type {type(review_count)}")

driver.quit()