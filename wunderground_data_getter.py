import requests
from bs4 import BeautifulSoup
import pickle

READ_FROM_DISK = True
#default carnation
#URL = "https://www.wunderground.com/weather/us/wa/carnation"
#tolt middle school station
URL = "https://www.wunderground.com/dashboard/pws/KWACARNA1"



if not READ_FROM_DISK:
    page = requests.get(URL)
    with open('page.pk1', 'wb') as out_file:
        pickle.dump(page, out_file)
else:
    with open('page.pk1', 'rb') as in_file:
        page = pickle.load(in_file) 

soup = BeautifulSoup(page.content, 'html.parser')
#current_temp = soup.find(id="_ngcontent-app-root-c122")
current_temp = soup.find(class_="wu-unit-temperature")
current_pressure = soup.find(class_="wu-unit-pressure")

class Wu_Data():
    def __init__(self, response_in):
        self.current_temp = self.pretify_and_strip(soup.find(class_="wu-unit-temperature").span)

        self.current_pressure = self.pretify_and_strip(soup.find(class_="wu-unit-pressure").span)
        self.today_precip = self.pretify_and_strip(soup.find(class_="wu-unit-rain").span)
        self.humidity = self.pretify_and_strip(soup.find(class_="wu-unit-humidity").span)
        print (self.current_pressure)
        print (self.current_temp)
        print (self.today_precip)
        print (self.humidity)


    def pretify_and_strip(self, data):

        data_div = data.prettify().split("<")
        data_div_list = data_div[1].splitlines()
        current_data = data_div_list[1].strip()
        return current_data



current_conditions = Wu_Data(soup)

