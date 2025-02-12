#%%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time as tm
import pandas as pd
import os
from openpyxl import Workbook
from datetime import datetime
#%%
def removeNonDigit(text):
    for char in text:
        if not char in "0123456789":
            text = text.replace(char,'')
    return text.strip()

def checkSheetExist(file_path,sheet_name):
    excel_file = pd.ExcelFile(file_path)
    # Check if the sheet name exists
    return sheet_name in excel_file.sheet_names


#%% BEGIN SCRAPPING
service = Service(ChromeDriverManager().install())
options = Options()
#options.add_argument("--headless")

#Search in google chrome
driver = webdriver.Chrome(service=service, options=options)
name = "pita lite military trail"
# open the google search page
driver.get("https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwi39uKNi5eJAxUcnYkEHUoYJPYQPAgI")
wait = WebDriverWait(driver,10)
tm.sleep(2)
search_bar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".gLFyf")))
search_bar.send_keys(name + " reviews")
search_bar.send_keys(Keys.RETURN)
tm.sleep(2)
#get the review count
review_count_string = driver.find_element(By.CSS_SELECTOR, ".hqzQac span a span").text
review_count = int(removeNonDigit(review_count_string))
print(review_count)


driver.quit()
#%%
print("starting the data writing")
#STORE THE DATA
curdir = os.getcwd()
path = os.path.join(curdir,"data")

#%% Check whether an excel file exist
print("checking whether data exist")
files = os.listdir(path)
file = [file for file in files if file.endswith(".xlsx")]
sheetName = name+ " sheet"
date = datetime.today().strftime('%Y-%d-%m')
if file:
    #check whether we already data for the current business
    excel_file_path = os.path.join(path,file[0])
    sheet_exist = checkSheetExist(excel_file_path,sheetName)
    with pd.ExcelWriter(excel_file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        if sheet_exist:
            print("updating an existing sheet")
            existing_data_df = pd.read_excel(excel_file_path, sheet_name=sheetName)
            use_linkup = input("Does this business use Link Up?: ")

            df = pd.DataFrame({'Review Count':[review_count],'Date':date,'With LinkUp':use_linkup})
            new_df = pd.concat([existing_data_df,df],axis=0)

            #write the new dataframe back the original excel sheet
            new_df.to_excel(writer, sheet_name=sheetName,index=False)
        else:
            print("adding a sheet to an existing file")
            # we create a new sheet
            use_linkup = input("Does this business use Link Up?: ")
            df = pd.DataFrame({'Review Count':[review_count],'Date':date,'With LinkUp':use_linkup})

            #write the new dataframe back the original excel sheet
            df.to_excel(writer, sheet_name=sheetName,index=False)
else:
    excel_file_path = os.path.join(path,"linkup_data.xlsx")
    print("excel file doesn't exist, create a new one")
    use_linkup = input("Does this business use Link Up?: ")
    df = pd.DataFrame({'Review Count':[review_count],'Date':date,'With LinkUp':use_linkup})
    df.to_excel(excel_file_path, sheet_name=sheetName, index=False)