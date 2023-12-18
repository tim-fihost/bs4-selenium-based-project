import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml
import time
link = 'https://appbrewery.github.io/Zillow-Clone/'
google_survey = "https://docs.google.com/forms/d/e/1FAIpQLSf9TB3aBDnw2bS6A-gr003jotnVLRjIBzRWzuM0Rp3a8iuaJA/viewform"
class DataScraper:
    def __init__(self):
        response = requests.get(link)
        self.soup = BeautifulSoup(response.text, 'lxml')
        self.get_info_price = self.get_info_prices()
        self.get_info_address = self.get_info_addresses()
        self.get_info_ref = self.get_info_refs()
        #selenium reqs
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(google_survey)
    
    #references
    def get_info_refs(self):    
        refs = self.soup.select('a.property-card-link')
        ref_list = []
        for element in refs:
            ref_list.append(element.get('href'))
        return ref_list
    
    def get_info_prices(self):
        prices = self.soup.select('span.PropertyCardWrapper__StyledPriceLine')
        prices_list = []
        for price in prices:
            prices_list.append(price.text.split('/')[0].split('+')[0])
        return prices_list

    def get_info_addresses(self):    
        # list of addresses
        addresses = self.soup.select('address')
        addresses_list = []
        for address in addresses:
            addresses_list.append(address.text.split('\n')[1].strip())
        return addresses_list
    
    #selenium auto fill
    def update(self):
        addresses = self.get_info_address
        prices = self.get_info_price    
        refs = self.get_info_ref
        time.sleep(2)
        for i in range(len(addresses)):
            #address
            address_insert = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            print(addresses[i])
            address_insert.send_keys(addresses[i])
            #price
            price_insert = self.driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            print(prices[i])
            price_insert.send_keys(prices[i])
            #references
            ref_insert = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            print(refs[i])
            ref_insert.send_keys(refs[i])
            
            
            submit = self.driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit.click()
            print("Has been inserted")
            self.driver.get(google_survey)

information = DataScraper()
information.update()
print("All DONE")