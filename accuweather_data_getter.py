import requests
import json
import accuweather_config as config


READ_FROM_FILE = False


AW_CURRENT_REQUEST = ("http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true" % (config.CARNATION_KEY, config.DEV_KEY))
## Looks like maybe they only allow 5 days and less?
AW_FORECAST_REQUEST = ("http://dataservice.accuweather.com/forecasts/v1/daily/5day/%s?apikey=%s&details=true" % (config.CARNATION_KEY, config.DEV_KEY))
LOCATION = 'Carnation'

#if not READ_FROM_FILE:
#    req = requests.get(AW_CURRENT_REQUEST)
#    with open('details.json', 'w') as out_file:
#        json.dump(req.json(), out_file)
#    details = req.json()
#else:
#    with open('details.json', 'r') as in_file:
#        details = json.load(in_file)
#

def make_call():
    """this makes the call for the current conditions"""
    req = requests.get(AW_CURRENT_REQUEST)
    return req.json()

def make_forecast_call():
    req = requests.get(AW_FORECAST_REQUEST)
    with open('forecast.json', 'w') as out_file:
        json.dump(req.json(), out_file)
    return req.json()



#print (details)

class AwData():
    def __init__(self, json_in):
        self.details = json_in
        self.apparent_temperature = json_in[0]["ApparentTemperature"]["Imperial"]["Value"]
        self.indoor_relative_humidity = json_in[0]["IndoorRelativeHumidity"]

        self.precip1hr = json_in[0]["Precip1hr"]["Imperial"]["Value"]
        self.precip = json_in[0]["PrecipitationSummary"]["Precipitation"]["Imperial"]["Value"]
        self.precip_past1 = json_in[0]["PrecipitationSummary"]["PastHour"]["Imperial"]["Value"]
        self.precip_past12 = json_in[0]["PrecipitationSummary"]["Past12Hours"]["Imperial"]["Value"]
        self.precip_past18 = json_in[0]["PrecipitationSummary"]["Past18Hours"]["Imperial"]["Value"]
        self.precip_past24 = json_in[0]["PrecipitationSummary"]["Past24Hours"]["Imperial"]["Value"]

        self.pressure = json_in[0]["Pressure"]["Imperial"]["Value"]
        self.pressure_tendency = json_in[0]["PressureTendency"]["LocalizedText"]
        self.feels_like_temp = json_in[0]["RealFeelTemperature"]["Imperial"]["Value"]
        self.relative_humidity = json_in[0]["RelativeHumidity"]
        self.temperature = json_in[0]["Temperature"]["Imperial"]["Value"]
        self.wet_bulb_temperature = json_in[0]["WetBulbTemperature"]["Imperial"]["Value"]
        self.wind_direction = json_in[0]["Wind"]["Direction"]["Degrees"]
        self.wind_speed = json_in[0]["Wind"]["Speed"]["Imperial"]["Value"]
        self.location = LOCATION

        ### These are new attributes and need to be stored
        self.dew_point = json_in[0]["DewPoint"]["Imperial"]["Value"]
        self.temperature_past_12_max = json_in[0]["TemperatureSummary"]["Past12HourRange"]["Maximum"]["Imperial"]["Value"]
        self.temperature_past_12_min = json_in[0]["TemperatureSummary"]["Past12HourRange"]["Minimum"]["Imperial"]["Value"]
        self.temperature_past_24_max = json_in[0]["TemperatureSummary"]["Past24HourRange"]["Maximum"]["Imperial"]["Value"]
        self.temperature_past_24_min = json_in[0]["TemperatureSummary"]["Past24HourRange"]["Minimum"]["Imperial"]["Value"]


        



    def __str__(self):
        out_text = "Precipition right now is: " + str(self.precip1hr)
        out_text += "\nThe Temperature right now is : "  + str(self.temperature)
        out_text += "\nThe Humidity right now is: " +  str(self.relative_humidity)
        out_text += "\nThe Precipitaiton in the last 24 hours is: " + str(self.precip_past24)
        #print ("The Precipitaiton in the last 12 hours is: ", self.PrecipPast12)
        out_text += "\nThe Pressure is %s and it is trending %s." % (self.pressure, self.pressure_tendency)
        out_text += "\nThe high temperature in the past 24 hours is: " + str(self.temperature_past_24_max)
        out_text += "\nThe low temperature in the past 24 hours is : " + str(self.temperature_past_12_min)
        return out_text
        #print (self.IndoorRelativeHumidity)
        #print (self.ApparentTemperature)

    def get_data_dict(self):
        data_dict = {}
        data_dict['hour_precip'] = self.precip1hr
        #data_dict['humidity'] = self.humidity
        data_dict['temperature'] = self.temperature
        data_dict['12_hour_precip'] = self.precip_past12
        data_dict['24_hour_precip'] = self.precip_past24
        data_dict['pressure'] = self.pressure
        data_dict['pressure_tendancy'] = '"' + self.pressure_tendency + '"'
        data_dict['apparent_temperature'] = self.apparent_temperature
        data_dict['indoor_relative_humidity'] = self.indoor_relative_humidity
        data_dict['feels_like_temperature'] = self.feels_like_temp
        data_dict['relative_humidity'] = self.relative_humidity
        data_dict['wet_bulb_temperature'] = self.wet_bulb_temperature
        data_dict['wind_direction'] = self.wind_direction
        data_dict['wind_speed'] = self.wind_speed
        data_dict['location'] = '"' + self.location + '"'

        data_dict['dew_point'] = self.dew_point
        data_dict['temperature_max_past_12'] = self.temperature_past_12_max
        data_dict['temperature_min_past_12'] = self.temperature_past_12_min
        data_dict['temperature_max_past_24'] = self.temperature_past_24_max
        data_dict['temperature_min_past_24'] = self.temperature_past_24_min


        return data_dict

#current = Aw_Data(details)
        




if __name__ == "__main__":
    details = make_call()
    current = AwData(details)
    print (current)
    forecast = make_forecast_call()


""" to do:
    figure out some way to store data for now.
    Start parsing response.
    look into other data sources"""



