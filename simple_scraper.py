# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:07:19 2023

@author: socia
"""

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options )

driver.get('https://www.totaljobs.com/jobs/in-europe?radius=10&searchOrigin=Resultlist_top-search')

element = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'res-1na8b7y'))
)


job_link_elements = driver.find_elements(By.CLASS_NAME, 'res-1na8b7y')
job_title_elements = driver.find_elements(By.CLASS_NAME, 'res-nehv70')
job_company_elements = driver.find_elements(By.CLASS_NAME, 'res-1j1rn10')
job_place_elements = driver.find_elements(By.CLASS_NAME, 'res-1qil8oy')
job_salary_elements = driver.find_elements(By.CLASS_NAME, 'res-1qil8oy')


job_links = [element.get_attribute('href') for element in job_link_elements]
print(job_links)
job_titles = [element.text for element in job_title_elements]
print(job_titles)
job_companies = [element.text for element in job_company_elements]
print(job_companies)
job_places = [element.text for element in job_place_elements if element.get_attribute('data-at') == 'job-item-location']
print(job_places)
job_salaries = [element.text for element in job_salary_elements if element.get_attribute('data-at') == 'job-item-salary-info']
print(job_salaries)

driver.quit()
print(1)