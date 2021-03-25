import requests
#from bs4 import BeautifulSoup
import json
import pickle
import datetime


READ_FROM_DISK = False


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
    apikey = '6532d6454b8aa370768e63d6ba5a832e' 
    location_cords = '47.45%2C-122.31'
    URL = "https://api.weather.com/v3/wx/forecast/daily/15day?apiKey={0}&geocode={1}&language=en-US&units=e&format=json".format(apikey, location_code)

    if not READ_FROM_DISK:
        r = requests.get(URL, headers=headers)
        with open('forecast_results.pk1', 'wb') as out_file:
            pickle.dump(r, out_file)
    else:
        with open('forecast_results.pk1', 'rb') as in_file:
            r = pickle.load(in_file)
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
            fifteen_day_dict['date_gathered'] = str(datetime.datetime.now())[:-4]
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
            fifteen_day_dict['wind_direction_cardinal_day'] = inner["windDirectionCardinal"][index*2]
            fifteen_day_dict['wind_direction_night'] = inner["windDirection"][index*2-1]
            fifteen_day_dict['wind_direction_cardinal_night'] = inner["windDirectionCardinal"][index*2-1]
            fifteen_day_dict['wind_speed_day'] = inner["windSpeed"][index*2]
            fifteen_day_dict['wind_speed_night'] = inner["windSpeed"][index*2-1]
            fifteen_day_dict['cloud_cover_chance_day'] = inner["cloudCover"][index*2]
            fifteen_day_dict['cloud_cover_chance_night'] = inner["cloudCover"][index*2-1]

            for item in fifteen_day_dict:
                if fifteen_day_dict[item] == '':
                    fifteen_day_dict[item] = None
                if type(fifteen_day_dict[item]) == str:
                    # this also changes datetime. maybe need to fix that. check with mysql_examiner (add table) and see
                    fifteen_day_dict[item] = '"' + fifteen_day_dict[item] + '"'
                    if '~' in fifteen_day_dict[item]:
                        fifteen_day_dict[item] = fifteen_day_dict[item].replace('~','')
                    if '<' or '>' in fifteen_day_dict[item]:
                        fifteen_day_dict[item] = fifteen_day_dict[item].replace('<','')
                        fifteen_day_dict[item] = fifteen_day_dict[item].replace('>','')

                # This converts none types into 0.0 for mysql. Not sure if this is the right behavior
                if fifteen_day_dict[item] == None:
                    fifteen_day_dict[item] = 0.0
               #     fifteen_day_dict[item] = None
            self.fifteen_day_list.append(fifteen_day_dict)

    def get_dict_list(self):
        return self.fifteen_day_list







if __name__=="__main__":
    forecast_data = make_call('location')
    forecast_object = WuForecast(forecast_data)
    #forecast_data = WuForecast(response_data)


