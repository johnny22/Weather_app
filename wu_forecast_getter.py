import requests
#from bs4 import BeautifulSoup
import json
import pickle


READ_FROM_DISK = False

apikey = '6532d6454b8aa370768e63d6ba5a832e' 
URL = "https://api.weather.com/v3/wx/forecast/daily/fifteenday?apiKey={}&geocode=47.45%2C-122.31&language=en-US&units=e&format=json".format(apikey)


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

def make_call(location_code):
    """ for now, we will ignore location_code, but we will want to implement that in the future"""


    if not READ_FROM_DISK:
        r = requests.get(URL, headers=headers)
        with open('forecast_results.pk1', 'wb') as out_file:
            pickle.dump(r, out_file)
    else:
        with open('forecast_results.pk1', 'rb') as in_file:
            r = pickle.load(in_file)
    print (r.content)
    response_data = json.loads(r.content)
    #with open('out.json', 'w') as json_out:
    #    json_out.write(json.dumps(response_data))
    return response_data
    

    

class WuForecast():
    def __init__(self, response_in):
        self.web_data = response_in
        self.fifteen_day_list = []
        #self.fifteenday_dict = {}
        self.create_dict_list()
       # for x in self.fifteen_day_list:
       #     for k in x:
       #         print (k, ': ', x[k])
       #     print ('#'*50)


    def create_dict_list(self):
        inner = self.web_data["daypart"][0]
        for index in range(len(self.web_data["validTimeLocal"])):
            fifteen_day_dict= {}
            #out_list = [
            fifteen_day_dict['date_forecast'] = self.web_data["validTimeLocal"][index][0:10]
            fifteen_day_dict['max_temp'] = self.web_data["temperatureMax"][index]
            fifteen_day_dict['min_temp'] = self.web_data["temperatureMin"][index]
            fifteen_day_dict['qpf'] = self.web_data["qpf"][index]
            fifteen_day_dict['precip_type_day'] = inner["precipType"][index*2]
            fifteen_day_dict['precip_type_night'] = inner["precipType"][index*2-1]
            fifteen_day_dict['precip_chance_day'] = inner["precipChance"][index*2]
            fifteen_day_dict['precip_chance_night'] = inner["precipChance"][index*2-1]
            fifteen_day_dict['relative_humidity_day'] = inner["relativeHumidity"][index*2]
            fifteen_day_dict['relative_humidity_night'] = inner["relativeHumidity"][index*2-1]
            fifteen_day_dict['wx_phrase_day'] = inner["wxPhraseLong"][index*2]
            fifteen_day_dict['wx_phrase_night'] = inner["wxPhraseLong"][index*2-1]
            fifteen_day_dict['snow_amount_day'] = inner["snowRange"][index*2]
            fifteen_day_dict['snow_amount_night'] = inner["snowRange"][index*2-1]
            fifteen_day_dict['wind_direction_day'] = inner["windDirection"][index*2]
            fifteen_day_dict['wind_direction_night'] = inner["windDirection"][index*2-1]
            fifteen_day_dict['wind_speed_day'] = inner["windSpeed"][index*2]
            fifteen_day_dict['wind_speed_night'] = inner["windSpeed"][index*2-1]
            fifteen_day_dict['cloud_cover_chance_day'] = inner["cloudCover"][index*2]
            fifteen_day_dict['cloud_cover_chance_night'] = inner["cloudCover"][index*2-1]

            
            self.fifteen_day_list.append(fifteen_day_dict)

        def get_dict_list(self):
            return self.fifteen_day_list







if __name__=="__main__":
    forecast_data = WuForecast(response_data)


