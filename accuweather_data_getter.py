import requests
import json
import accuweather_config as config


READ_FROM_FILE = True


AW_CURRENT_REQUEST = ("http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true" % (config.CARNATION_KEY, config.DEV_KEY))

if not READ_FROM_FILE:
    req = requests.get(AW_CURRENT_REQUEST)
    print ("We don't get here, right?")
    with open('details.json', 'w') as out_file:
        json.dump(req.json(), out_file)
    details = req.json()
else:
    with open('details.json', 'r') as in_file:
        details = json.load(in_file)

#print (details)

class Aw_Data():
    def __init__(self, json_in):
        self.details = json_in
        self.ApparentTemperature = json_in[0]["ApparentTemperature"]["Imperial"]["Value"]
        self.IndoorRelativeHumidity = json_in[0]["IndoorRelativeHumidity"]

        self.Precip1hr = json_in[0]["Precip1hr"]["Imperial"]["Value"]
        self.Precip = json_in[0]["PrecipitationSummary"]["Precipitation"]["Imperial"]["Value"]
        self.PrecipPast1 = json_in[0]["PrecipitationSummary"]["PastHour"]["Imperial"]["Value"]
        self.PrecipPast12 = json_in[0]["PrecipitationSummary"]["Past12Hours"]["Imperial"]["Value"]
        self.PrecipPast18 = json_in[0]["PrecipitationSummary"]["Past18Hours"]["Imperial"]["Value"]
        self.PrecipPast24 = json_in[0]["PrecipitationSummary"]["Past24Hours"]["Imperial"]["Value"]

        self.Pressure = json_in[0]["Pressure"]["Imperial"]["Value"]
        self.PressureTendency = json_in[0]["PressureTendency"]["LocalizedText"]
        self.FeelsLikeTemp = json_in[0]["RealFeelTemperature"]["Imperial"]["Value"]
        self.RelativeHumidity = json_in[0]["RelativeHumidity"]
        self.Temperature = json_in[0]["Temperature"]["Imperial"]["Value"]
        self.WetBulbTemperature = json_in[0]["WetBulbTemperature"]["Imperial"]["Value"]
        self.WindDirection = json_in[0]["Wind"]["Direction"]["Degrees"]
        self.WindSpeed = json_in[0]["Wind"]["Speed"]["Imperial"]["Value"]
        print ("Precipitation right now is: ", self.Precip1hr)
        print ("The temperature right now is: ", self.Temperature)
        print ("The Humidity right now is: ", self.RelativeHumidity)
        print ("The Precipitaiton in the last 24 hours is: ", self.PrecipPast24)
        print ("The Precipitaiton in the last 12 hours is: ", self.PrecipPast12)
        print ("The Pressure is %s and it is trending %s." % (self.Pressure, self.PressureTendency))
        print (self.IndoorRelativeHumidity)
        print (self.ApparentTemperature)


current = Aw_Data(details)
        






""" to do:
    figure out some way to store data for know.
    Start parsing response.
    look into other data sources"""



