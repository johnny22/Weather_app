import requests
import pickle
import json




def make_call(location):

    apikey = 'e1f10a1e78da46f5b10a1e78da96f525'
    URL = 'https://api.weather.com/v2/pws/observations/current?apiKey={0}&stationId={1}&numericPrecision=decimal&format=json&units=e'.format(apikey, location)

    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.fifteen (KHTML, like Gecko) Version/14.0.2 Safari/605.1.fifteen",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            #"referrer": "https://www.wunderground.com/calendar/us/wa/carnation",
            "method": "GET",
            "mode": "cors"
        }

    r = requests.get(URL, headers=headers)
    if r.status_code == 200:
        response_data = json.loads(r.content)
        return response_data
    else:
        print ("Ignored : " + str(location))
        return None

class WuData():
    def __init__(self, response_in, location):
        """this takes json in """
        self.out_dict = {}
        self.out_dict['location'] = '"' + location + '"'
        data = response_in['observations'][0]['imperial']
        self.current_temp = data['temp']
        self.out_dict['current_temp'] = data['temp']
        self.out_dict['current_pressure'] = data['pressure']
        self.out_dict['today_precip'] = data['precipTotal']
        self.out_dict['current_humidity'] = response_in['observations'][0]['humidity']
        self.out_dict['wind_speed'] = data['windSpeed']
        self.out_dict['wind_direction'] = response_in['observations'][0]['winddir']
        self.out_dict['wind_gust'] = data['windGust']
        self.out_dict['wind_chill'] = data['windChill']
        self.out_dict['dew_point'] = data['dewpt']
        self.current_pressure = data['pressure']
        self.today_precip = data['precipTotal']
        self.humidity = response_in['observations'][0]['humidity']
        self.wind_speed = data['windSpeed']
        self.wind_direction = response_in['observations'][0]['winddir']
        self.wind_gust = data['windGust']
        self.wind_chill = data['windChill']
        self.dew_point = data['dewpt']




if __name__ == "__main__":
    location_list = ['KWACARNA1', 'KWAFALLC80']
    page_list = []
    for location in location_list:
        page = make_call(location)
        page_list.append((page, location))


    for tup in page_list:
        conditions = WuData(tup[0], tup[1])
        print (conditions.out_dict)

