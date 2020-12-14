from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


data = pd.read_csv('Sample Input.csv')


class Scraper:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def CloseBrowser(self):
        time.sleep(5)
        self.driver.close()

    def getData(self):
        employees = []
        links = []
        company_names = []
        driver = self.driver
        site = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        driver.get(site)
        username = driver.find_element_by_xpath(
            '//*[contains(@aria-label, "Email or Phone")]')
        password = driver.find_element_by_xpath(
            '//*[contains(@aria-label, "Password")]')
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(2)

        for link in data['Profile Page'].to_list():
            try:
                driver.get(link)
                soup = bs4(driver.page_source, 'html.parser')
                content = soup.find('span', {'class': 'v-align-middle'})
                companyName = soup.find(
                    'h1', {'class': 'top-card-layout__title'})
                if not content:
                    employees.append('N/A')
                    links.append(link)
                employees.append(content.text.split(' ')[14])
                links.append(link)

            except Exception as e:
                pass

        for name in data['Company']:
            company_names.append(name)

        print(links, employees, company_names)
        linkedInData = {'Company': company_names,
                        'Profile Page': links, 'Employee count': employees}
        df = pd.DataFrame(linkedInData)
        return df.to_csv('linkedIn2.csv')


if __name__ == '__main__':
    username = input('Enter username:')
    password = input('Enter password:')
    get = Scraper(username, password)
    get.getData()
