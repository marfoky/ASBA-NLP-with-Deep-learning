"""Selenium bot."""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from db_code import EmploymentSituationDB

URL = "https://www.bls.gov/bls/news-release/empsit.htm"
db_service = EmploymentSituationDB("main.db")
options = Options()
options.add_argument("--no-sandbox")
# options.add_argument("--headless=new")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.get(URL)

years_to_scrape = [
    "2024",
    "2023",
    "2022",
    "2021",
    "2020",
    "2019",
    "2018",
    "2017",
    "2016",
    "2015",
    "2014",
    "2013",
    "2012",
    "2011",
    "2010",
    "2009",
    "2008",
    "2007",
]

try:
    for year in years_to_scrape:
        year_section = driver.find_element(By.ID, year)

        links = year_section.find_elements(
            By.XPATH, f".//following-sibling::ul[1]//li/a[1]"
        )

        for link in links:
            month_year_text = link.text.strip()
            print(f"Processing: {month_year_text}")

            link.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            page_content = driver.find_element(By.TAG_NAME, "body").text

            db_service.save_to_db(month_year_text, page_content)

            print(f"Saved: {month_year_text}")

            driver.back()

            time.sleep(1)

finally:
    # Close the driver after completion
    driver.quit()
