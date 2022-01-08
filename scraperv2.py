from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import time
import csv
import psycopg2



def CheckRange ( element):
    if len(element)==0:
        return "NULL"
    else:
        return element[0].text

def innerHtml ( element):
    if len(element)==0:
        return "NULL"
    else:
        return element[0].get_attribute('innerHTML')

def scrap_LinkedIn(index):
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=0")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    url = "https://www.linkedin.com/jobs/search/?geoId=105015875&location=France"+ str(index)
    driver.get(url)
    time.sleep(2)
    #driver.add_cookie({"name": "li_at", "value": "AQEDARyCsCMAtjtOAAABfGLc4o0AAAF-XSiboU4AXz_AFJkjMuWDw3f_Xg51EO-zTQCiGa7TC1PIuniyiazBV1miHw2Qb4D-I_eCCws6mlTExwX8foYHFe6ybwqoHvH7heeO0Vxvbhmg8Hy8odJ7B6mV"})
    search__results = driver.find_elements_by_xpath('//*[@id="main-content"]/section/ul')
    jobs=[]
    for li in search__results:
        lnks=driver.find_elements_by_tag_name("a")
        for lnk in lnks:
            job_link = lnk.get_attribute("href")
            if "https://fr.linkedin.com/jobs/view" in job_link:
                jobs.append(job_link)
    jobs_details = []
    for job in jobs:


            #driver.add_cookie({"name": "li_at", "value": "AQEDARyCsCMAtjtOAAABfGLc4o0AAAF-XSiboU4AXz_AFJkjMuWDw3f_Xg51EO-zTQCiGa7TC1PIuniyiazBV1miHw2Qb4D-I_eCCws6mlTExwX8foYHFe6ybwqoHvH7heeO0Vxvbhmg8Hy8odJ7B6mV"})
            driver.get(job)
            time.sleep(3)
            job_title        = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/section[2]/div/div[2]/div/h1'))

            job_company      = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/section[2]/div/div[2]/div/h4/div[1]/span[1]'))
            job_location     = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/section[2]/div/div[2]/div/h4/div[1]/span[2]'))
            Seniority        = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/div[1]/section/div/ul/li[1]/span'))
            Employment_type  = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/div[1]/section/div/ul/li[2]/span'))
            Job_function     = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/div[1]/section/div/ul/li[3]/span'))
            Industries       = CheckRange(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/div[1]/section/div/ul/li[4]/span'))
            job_description  = innerHtml(driver.find_elements_by_xpath('//*[@id="main-content"]/section[1]/div/div[1]/section/div/div/section/div'))
            if job_title!='NULL':
                jobs_details.append({ job_title, job_location,  job_company, Seniority, job_description, Employment_type})
                conn = psycopg2.connect( database="postgres", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
                conn.autocommit = True
                cursor = conn.cursor()
                postgres_insert_query  =""" INSERT INTO public.jobs(job_title, job_company, job_location, seniority, employment_type, job_function, industries, job_description) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"""
                record_to_insert = (job_title, job_company, job_location, Seniority, Employment_type, Job_function, Industries, job_description)
                cursor.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                conn.close()
            time.sleep(3)


indexes = [0, 25, 50, 75, 100, 125, 150]
for i in indexes:
    scrap_LinkedIn(25)
