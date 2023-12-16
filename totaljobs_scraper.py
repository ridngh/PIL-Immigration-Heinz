# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:07:19 2023

@author: socia
"""
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from numpy import random
from time import sleep


def navigate_browser(main_url, o_file):
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)  
    #options.page_load_strategy = 'none'
    #driver.implicitly_wait(60)
    driver.maximize_window()
    print('Driver initialised')
    
    driver.get(main_url)
    print('Site Loaded')
    
    driver.find_element(By.ID, 'ccmgt_explicit_preferences').click()
    driver.find_element(By.ID, 'ccmgt_preferences_reject').click()
    print('Cookies Rejected')
    
    scrape_website(driver, o_file, 'w')
    next_pg_button = check_next_page(driver)
    
    while next_pg_button:
        sleeptime = random.uniform(2, 4)
        print("sleeping for:", sleeptime, "seconds")
        sleep(sleeptime)
        print("sleeping is over")
        
        driver.execute_script('arguments[0].click()', next_pg_button)
        scrape_website(driver, o_file, 'a')
        next_pg_button = check_next_page(driver)
     
    # The code has been tested with a break condition as there are multiple
    # result pages and it was not feasible to go through all of them
        break
               
    driver.quit()
    print('Driver Closed')


    
def scrape_website(driver, o_file, mode):
    print('Scraping website')
    # totaljobs displays job links, waiting for job links to appear
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'res-1na8b7y')))

    job_link_elements = driver.find_elements(By.CLASS_NAME, 'res-1na8b7y')
    links = [element.get_attribute('href') for element in job_link_elements]
    
    job_title_elements = driver.find_elements('xpath',
                                              '//*[starts-with(@id, "job-item")]/div[1]/h2/a/div/div/div')
    titles = [element.text for element in job_title_elements]
    
    job_company_elements = driver.find_elements('xpath', 
                                              '//*[starts-with(@id, "job-item")]/div[1]/div[2]/span')
    companies = [element.text for element in job_company_elements]
    
    job_place_elements = driver.find_elements('xpath', 
                                              '//*[starts-with(@id, "job-item")]/div[1]/div[3]/div[1]/div[1]/span/span')
    locations = [element.text for element in job_place_elements]
    
    job_salary_elements = driver.find_elements('xpath', 
                                              '//*[starts-with(@id, "job-item")]/div[1]/div[3]/div[2]/span')
    salaries = [element.text for element in job_salary_elements]
    
    job_description_elements = driver.find_elements('xpath', 
                                              '//*[starts-with(@id, "job-item")]/div[2]/div[1]/span/div/div[1]/span')
    descriptions = [element.text for element in job_description_elements]   
    # descriptions = [scrape_jobpage(driver, link) for link in links]

    write_csv(links,titles,companies,locations,salaries,descriptions, o_file, mode)

def write_csv(links,titles,companies,locations,salaries,descriptions, o_file, mode):
    print('Writing scraped data')
    df = pd.DataFrame({'Job Link': links,
                       'Job Title': titles,
                       'Job Company': companies,
                       'Job Location': locations,
                       'Salary': salaries,
                       'Description': descriptions})
    
    if mode == 'w':
        df.to_csv(o_file, mode = mode, encoding = 'utf-8-sig', index=False)
    else:
       df.to_csv(o_file, mode = mode, encoding = 'utf-8-sig', header=False
                 , index=False)



def check_next_page(driver):
    print('Checking for next pg')
    pgnav_button_elements = driver.find_elements(By.CLASS_NAME, 'res-k0fpyx')
    
    try:
        nxt_pg_button = [element for element in pgnav_button_elements 
                         if element.get_attribute('aria-label') == 'Next' 
                         and element.get_attribute('href') is not None][0]
        
        print('Next pg found')
        return nxt_pg_button   

    except:        
        print('No next pg found')           
        return False


        
def main():
    main_url = 'https://www.totaljobs.com/jobs/in-europe?radius=10&searchOrigin=Resultlist_top-search'
    o_file = 'total_jobs_data.csv'
    navigate_browser(main_url,o_file)

main()


# =============================================================================
# CODE WORK IN PROGRESS
# =============================================================================
# DESCRIPTION: This function aimed to open each job link & scrape job description
# =============================================================================
# REASON OF FAILURE: The job links keep loading continuously.
# With each reload a suffix beginning with '&v=' gets added to the url.
# =============================================================================
# SOLUTIONS TRIED: - Set page loading strategy as None and eager
#                  - Add an implicit time wait
#                  - Cancel reload by pressing escape/using javascript
# =============================================================================

# from selenium.webdriver.common.keys import Keys
#
# def scrape_jobpage(driver, link):
#     sleeptime = random.uniform(2, 4)
#     print("sleeping for:", sleeptime, "seconds")
#     sleep(sleeptime)
#     print("sleeping is over")
#     
#     print('Scraping Jobpage')
#     driver.execute_script("window.open('');") 
#     driver.switch_to.window(driver.window_handles[1])
#     driver.get(link)
#     webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#     job_description = driver.find_elements(By.TAG_NAME, 'body').text
#
#     try:
#         job_description = job_description.text.split('Apply')[1]
#     except:
#         job_description = ''
#     
#     driver.close()
#     driver.switch_to.window(driver.window_handles[0])
#
#     return job_description
#
# 
#     # Had initially tried to mimic a human user by opening the job link in a
#     # a new tab by doing a right click
#     #ActionChains(driver).key_down(Keys.CONTROL).click(element).perform()
# 
#
#
# =============================================================================
# ========================================================
# REFERENCES
# https://www.zenrows.com/blog/selenium-python-web-scraping#headless-chrome
# https://www.blog.datahut.co/post/xpath-for-web-scraping-step-by-step-tutorial
# https://medium.com/@pawaraniket94334/web-scraping-using-selenium-3c8dadece905
# https://iqss.github.io/dss-webscrape/finding-web-elements.html
# https://www.zenrows.com/blog/selenium-python-web-scraping#fill-form
# https://stackoverflow.com/questions/11908249/debugging-element-is-not-clickable-at-point-error
# https://www.geeksforgeeks.org/opening-and-closing-tabs-using-sele
# https://stackoverflow.com/questions/62148505/how-to-right-click-on-a-link-and-open-the-link-in-a-new-tab-using-selenium-throu
# https://stackoverflow.com/questions/54501445/i-want-to-right-click-and-open-link-in-new-tab-using-selenium-with-python
# https://stackoverflow.com/questions/31876672/stop-infinite-page-load-in-selenium-webdriver-python
# https://stackoverflow.com/questions/71098316/stopping-page-loading-selenium-python
# https://stackoverflow.com/questions/66358904/stop-infinite-page-load-in-selenium-webdriver-python
# https://stackoverflow.com/questions/17533024/how-to-set-selenium-python-webdriver-default-timeout
# https://stackoverflow.com/questions/4054254/how-to-add-random-delays-between-the-queries-sent-to-google-to-avoid-getting-blo
# =============================================================================
