import mysql_config
import mysql.connector
from mysql.connector import errorcode
import datetime
import os


cnx = mysql.connector.connect(**mysql_config.config)


class examiner():
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.wunderground_forecast_column_list = [
        'date_gathered',
        'date_forecast',
        'max_temp',
        'min_temp',
        'qpf',
        'precip_type_day',
        'precip_type_night',
        'precip_chance_day',
        'precip_chance_night',
        'relative_humidity_day',
        'relative_humidity_night',
        'wx_phrase_day',
        'wx_phrase_night',
        'snow_amount_day',
        'snow_amount_night',
        'wind_direction_day',
        'wind_direction_night',
        'wind_speed_day',
        'wind_speed_night',
        'cloud_cover_chance_day',
        'cloud_cover_chance_night'
        ]

        self.get_wu_current_data()
        #self.get_current_data()
        #self.get_wu_forecast()


    def __str__(self):
        forecast = False



        if forecast:
            output = ''
            for line in self.wu_forecast_data:
                for entry in self.wunderground_forecast_column_list:
                    output += entry + ": " + str(line[self.wunderground_forecast_column_list.index(entry)])
                    if entry == 'precip_chance_night' or entry == 'wind_direction_night':
                        output +='\n'
                    elif entry == 'cloud_cover_chance_night':
                        output += '\n' + '#'*50 + '\n'
                    else:
                        output += '   '
                output +='\n'
            return output
        else:
            output = ''
            for line in self.data[:20]:
                #print (line)
                for entry in self.data_list:
                    output += entry + ": " + str(line[self.data_list.index(entry)])
                    output += '     '
                output +='\n'
            return output

    def get_wu_current_data(self):
        table = {39: None, 91: None, 93: None}
        self.data_list = ['date', 'location', 'current_pressure', 'current_temp', 'today_precip', 'current_humidity', 'wind_speed', 'wind_direction', 'wind_gust', 'wind_chill', 'dew_point']
        sql = "SELECT {} FROM wunderground ORDER BY date DESC".format(str(self.data_list).translate(table))
        print(sql)
        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()

    def get_wu_forecast(self):
        table = {39: None, 91: None, 93: None}
        sql = "SELECT {} FROM wunderground_forecast ORDER BY date_gathered DESC".format(str(self.wunderground_forecast_column_list).translate(table))
        print(sql)
        self.cursor.execute(sql)
        self.wu_forecast_data = self.cursor.fetchall()


    def get_current_data(self):
        #print (self.data)
        out_dict = {}
        x = 0
        inc = 0
        for key in self.data_list:
            out_dict[key] = self.data[x][inc]
            inc +=1
            #print (inc)
            #print (out_dict)
        self.current_conditions = out_dict
        #print (out_dict)




out = examiner(cnx)
print (out)
