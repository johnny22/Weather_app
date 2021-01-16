import requests
from bs4 import BeautifulSoup
import json
import pickle


READ_FROM_DISK = True


URL = "https://api.weather.com/v3/wx/forecast/daily/fifteenday?apiKey=6532d6454b8aa370768e63d6ba5a832e&geocode=47.45%2C-122.31&language=en-US&units=e&format=json"


headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.fifteen (KHTML, like Gecko) Version/14.0.2 Safari/605.1.fifteen",
        #"apiKey" : "6532d6454b8aa370768e63d6ba5a832e",
        #"geocode" : "47.45%2C-122.31",
        #"units" :   "e",
        #"format" : "json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "referrer": "https://www.wunderground.com/calendar/us/wa/carnation",
        "method": "GET",
        "mode": "cors"
    }



if not READ_FROM_DISK:
    r = requests.get(URL, headers=headers)
    with open('forecast_results.pk1', 'wb') as out_file:
        pickle.dump(r, out_file)
else:
    with open('forecast_results.pk1', 'rb') as in_file:
        r = pickle.load(in_file)


#soup = BeautifulSoup(r.content, 'html.parser')
response_data = json.loads(r.content)
with open('out.json', 'w') as json_out:
    json_out.write(json.dumps(response_data))

class WuForecast():
    def __init__(self, response_in):
        self.web_data = response_in
        self.fifteen_day_list = []
        #self.fifteenday_dict = {}
        self.create_dict_list()
        for x in self.fifteen_day_list:
            for k in x:
                print (k, ': ', x[k])
            print ('#'*50)


    def create_dict_list(self):
        inner = self.web_data["daypart"][0]
        for index in range(len(self.web_data["validTimeLocal"])):
            fifteen_day_dict= {}
            #out_list = [
            fifteen_day_dict['date'] = self.web_data["validTimeLocal"][index][0:10]
            fifteen_day_dict['high'] = self.web_data["temperatureMax"][index]
            fifteen_day_dict['low'] = self.web_data["temperatureMin"][index]
            fifteen_day_dict['qpfFullDay'] = self.web_data["qpf"][index]
            fifteen_day_dict['precipTypeD'] = inner["precipType"][index*2]
            fifteen_day_dict['precipTypeN'] = inner["precipType"][index*2-1]
            fifteen_day_dict['precipChanceD'] = inner["precipChance"][index*2]
            fifteen_day_dict['precipChanceN'] = inner["precipChance"][index*2-1]
            fifteen_day_dict['relativeHumidityD'] = inner["relativeHumidity"][index*2]
            fifteen_day_dict['relativeHumidityN'] = inner["relativeHumidity"][index*2-1]
            fifteen_day_dict['wxPhraseD'] = inner["wxPhraseLong"][index*2]
            fifteen_day_dict['wxPhraseN'] = inner["wxPhraseLong"][index*2-1]
            fifteen_day_dict['snowAmountD'] = inner["snowRange"][index*2]
            fifteen_day_dict['snowAmountN'] = inner["snowRange"][index*2-1]
            fifteen_day_dict['windDirectionD'] = inner["windDirection"][index*2]
            fifteen_day_dict['windDirectionN'] = inner["windDirection"][index*2-1]
            fifteen_day_dict['windSpeedD'] = inner["windSpeed"][index*2]
            fifteen_day_dict['windSpeedN'] = inner["windSpeed"][index*2-1]
            fifteen_day_dict['cloudCoverD'] = inner["cloudCover"][index*2]
            fifteen_day_dict['cloudCoverN'] = inner["cloudCover"][index*2-1]

            
            self.fifteen_day_list.append(fifteen_day_dict)







if __name__=="__main__":
    forecast_data = WuForecast(response_data)


