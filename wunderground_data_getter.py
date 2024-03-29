import requests
from bs4 import BeautifulSoup
import pickle

READ_FROM_DISK = False
#default carnation
#URL = "https://www.wunderground.com/weather/us/wa/carnation"
#tolt middle school station
#URL = "https://www.wunderground.com/dashboard/pws/KWACARNA1"
#LOCATION = 'KWACARNA1'


def make_call(url_code):
    url = "https://www.wunderground.com/dashboard/pws/" + url_code
    if not READ_FROM_DISK:
        page = requests.get(url)
        with open('page.pk1', 'wb') as out_file:
            pickle.dump(page, out_file)
    else:
        with open('page.pk1', 'rb') as in_file:
            page = pickle.load(in_file) 

    print("Status Code *************************")
    print(url_code)
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
    #current_conditions = Wu_Data(soup)
    #current_temp = soup.find(id="_ngcontent-app-root-c122")
    #current_temp = soup.find(class_="wu-unit-temperature")
    #current_pressure = soup.find(class_="wu-unit-pressure")

class WuData():
    def __init__(self, response_in, location):
        """response_in needs to be a soup object"""
        try:
            self.current_temp = self.pretify_and_strip(response_in.find(class_="wu-unit-temperature").span)
            self.current_pressure = self.pretify_and_strip(response_in.find(class_="wu-unit-pressure").span)
            self.today_precip = self.pretify_and_strip(response_in.find(class_="wu-unit-rain").span)
            self.humidity = self.pretify_and_strip(response_in.find(class_="wu-unit-humidity").span)
            #self.wind = self.pretify_and_strip(response_in.find(class_="wu-unit").span)
            self.location = location
            print (self.today_precip)
        except AttributeError as error:
            print(response_in)
            raise error
        #print (self.current_pressure)
        #print (self.current_temp)
        #print (self.today_precip)
        #print (self.humidity)


    def pretify_and_strip(self, data):

        data_div = data.prettify().split("<")
        data_div_list = data_div[1].splitlines()
        current_data = data_div_list[1].strip()
        return current_data


    def get_data_dict(self):
        data_dict = {}
        data_dict['current_pressure'] = self.current_pressure
        data_dict['current_temp'] = self.current_temp
        data_dict['today_precip'] = self.today_precip
        data_dict['current_humidity'] = self.humidity
        data_dict['location'] = '"' + self.location + '"'

        return data_dict


if __name__ == "__main__":
    #location_list = ['KWACARNA1', 'KWAFALLC80', 'KWAFALLC81']
    #location_list = ['KWACARNA1', 'KWAFALLC80']
    page_list = []
    for location in location_list:
        page = make_call(location)
        page_list.append((page, location))


    for tup in page_list:
        conditions = WuData(tup[0], tup[1])
        wunder_data = conditions.get_data_dict()
        #print (wunder_data)






