import mysql_config
import mysql.connector
from mysql.connector import errorcode
import datetime
import decimal
import plotly.express as px
import seaborn as sns
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import io
import time
#from base64 import b64encode

#server only
import os
import output_template


cnx = mysql.connector.connect(**mysql_config.config)


class wu_forecast():
    def __init__(self, connection):
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
        'wind_direction_cardinal_day',
        'wind_direction_night',
        'wind_direction_cardinal_night',
        'wind_speed_day',
        'wind_speed_night',
        'cloud_cover_chance_day',
        'cloud_cover_chance_night'
        ]
        self.date = str(datetime.datetime.now())[:-13]
        #print (datetime.datetime.now().date())

        self.connection = connection
        self.cursor = self.connection.cursor()
        self.get_forecast_data()
        self.out_list_test()


        


    def get_forecast_data(self):
        table = {39: None, 91: None, 93: None}
        # does this get every forecast from today, or only the last one?
        sql = "SELECT {0} FROM wunderground_forecast WHERE date_gathered LIKE '{1}%' ORDER BY date_forecast DESC".format(str(self.wunderground_forecast_column_list).translate(table), self.date)
        self.cursor.execute(sql)
        self.forecast_data = self.cursor.fetchall()

    def get_out_list(self):
        """this should return a list of dictionaries for each day"""
        out_list = []
        shortened_out_list = []
        x = 0
        for day in self.forecast_data:
            out_dict = {}
            inc = 0
            for key in self.wunderground_forecast_column_list:
                if key == 'date_forecast':
                    #day[inc] = day[inc].date()
                    out_dict[key] = day[inc].date()
                elif type(day[inc]) == decimal.Decimal and key != 'qpf':
                    out_dict[key] = str(day[inc])[:-3]
                else:
                    out_dict[key] = day[inc]
                inc += 1

            out_list.append(out_dict)

        last_date = self.get_last_gathered_date(out_list)


        for day in out_list:
            if day['date_gathered'] == last_date:
                shortened_out_list.append(day)

        shortened_out_list.reverse()
            

        return shortened_out_list

    def get_last_gathered_date(self, in_list):
        """ takes a list of all databse entries gathered this hour, and returns the date the last one was gathered on"""
        date_gathered_list = []
        #print (in_list)
        for out_day in in_list:
            for y in out_day:
                #print (y, ': ', out_day[y])
                if y == "date_gathered":
                    date_gathered_list.append(out_day[y])
        date_gathered_list = list(set(date_gathered_list))
        print (date_gathered_list)
        last_date = date_gathered_list[0]
        for date in date_gathered_list:
            if date > last_date:
                last_date = date
        return last_date


    def out_list_test(self):
        index = 0
        for forecast_day in self.forecast_data:
            #print (len(day))
            #print (type(day))
            for item in self.wunderground_forecast_column_list:
                #print (item[self.wunderground_forecast_column_list.index(item)], ': ', forecast_day)
                pass



class wunder_data():
    def __init__(self, connection, location):
        self.location = location
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.get_data()
        self.get_current_data()
        self.get_last_dates()
        self.get_weekly_precip()
        self.get_temp_list()
        #self.out_web_file()

    def __str__(self):
        output = ''
        for entry in self.data_list:
            output += entry + ": " + str(self.current_conditions[entry])
            output +='\n'
            #print (entry + " : ")
            #print (self.current_conditions[entry])
        output +=('Rainfall for the last 7 days :\n')
        #for entry in self.total_dict:
        #    #output += date.date + ": " + value
        #    #output += str(entry)
        #    output += str(entry.date()) + ": "
        #    #output += str(self.total_dict[entry]) + "\n"
        for entry in self.total_list:
            output += str(entry[0].date()) + ": " + str(entry[1]) + "\n"
            #output += str(
        output += ("\nTotal rainfall for this week is : " + str(self.weekly_precip))
        return output

    def get_temp_list(self):
        """Gets last temp:time list"""
        data_list = ['current_temp', 'date']
        temp_list = []
        day = datetime.datetime.now()
        from_day = day - datetime.timedelta(days=1)
        #location = 'KWACARNA1'
        sql = f"SELECT current_temp, date FROM wunderground WHERE date > '{str(from_day)}' and location='{self.location}' ORDER BY date DESC"
        self.cursor.execute(sql)
        info_list = self.cursor.fetchall()
        #print (info_list)
        time_list = []
        for item in info_list:
            time_list.append(np.datetime64(item[1]))
            temp_list.append(item[0])
        f_date = mpl.dates.DateFormatter('%H')
        print (self.location)
        #for x in time_list:
        #    print(x)
        print (len(time_list))
        print (len(temp_list))




        #Matplotlib
        #fig, ax  = plt.subplots(figsize=(3.5,3))
        #ax.plot(time_list, temp_list)
        #ax.xaxis.set_major_formatter(f_date)
        #ax.grid(visible=True, which='major')

        #fig.write_html('/var/www/weather_app/graph.html')
        #file_name = f'/var/www/weather_app/temp{self.location}.png'
        #fig.savefig(file_name)
        #self.graph = f'/temp{self.location}.png'

        #Plotlyexpress
        #file_name = f'/var/www/weather_app/temp{self.location}.html'
        #self.graph = f'/temp{self.location}.html'
        #print (time_list, temp_list)
        fig = px.line(x=time_list, y=temp_list, labels=dict(x="Time", y="Temperature"))
        #fig = sns.lineplot(x=time_list, y=temp_list)
        max_temp = temp_list[0]
        min_temp = temp_list[0]
        for temp in temp_list:
            if temp > max_temp:
                max_temp = temp
            if temp < min_temp:
                min_temp = temp

        for temp in temp_list:
            if temp == max_temp:
                ind = temp_list.index(temp)
                fig.add_annotation(x=time_list[ind], y=temp, text=str(temp))
            if temp == min_temp:
                ind = temp_list.index(temp)
                fig.add_annotation(x=time_list[ind], y=temp, text=str(temp))
        #print (plot(fig))
        #fig.write_html(file_name)
        buffer_s = io.StringIO()
        fig.write_html(buffer_s, include_plotlyjs='cdn')
        self.html_graph = buffer_s.getvalue()
        buffer_s.close()
        print (buffer_s.closed)
        del buffer_s
        del fig

        #print (type(self.html_graph))

    def template_out_dict(self):
        out_dict = {}
        rain_list = []
        for entry in self.data_list:
            out_dict[entry] = self.current_conditions[entry]
        for entry in self.total_list:
            out = (str(entry[0].date()), str(entry[1]))
            rain_list.append(out)
        out_dict['rain_list'] = rain_list
        if self.location =='KWACARNA1':
            out_dict['class'] = 'left'
        else:
            out_dict['class'] = 'right'

        out_dict['pressure_direction'] = self.get_point_list()
        print("Here")
        print(out_dict['today_precip'])
        out_dict['weekly_rain'] = str((self.weekly_precip + out_dict['today_precip']))
        #out_dict['temp_graph'] = str(self.graph)
        out_dict['html_graph'] = str(self.html_graph)
        return out_dict


    def out_web_file(self):
        with open('/var/www/weather_app/index.html', 'w') as out:
            out_text = '<html> \n <body> \n'
            for entry in self.data_list:
                out_text += '%s: %s  <br> \n' % (str(entry), str(self.current_conditions[entry]))

            out_text +=('Rainfall for the last 7 days :<br>\n')
            try:
                for entry in self.total_list:
                    out_text += str(entry[0].date()) + ": " + str(entry[1]) + "<br> \n"
                    #output += str(
                out_text += ("\nTotal rainfall for this week is : " + str(self.weekly_precip + self.current_conditions[self.data_list[3]]) + "<br>")
            except AttributeError:
                out_text += ("\n There is not enough data for total rainfall yet, please check back later.")
            
            out_text += '</html> \n </body> \n'
            out.write(out_text)

    def get_data(self):
        table = {39: None, 91: None, 93: None}
        self.data_list = ['date', 'location', 'current_pressure', 'current_temp', 'today_precip', 'current_humidity', 'wind_speed', 'wind_direction', 'wind_gust', 'wind_chill', 'dew_point']
        #sql = f"SELECT {str(self.data_list).translate(table)} FROM wunderground WHERE location='{self.location}' ORDER BY date DESC"

        now = datetime.datetime.now()
        first_date = now - datetime.timedelta(days=8)
        #print (first_date)
        sql = f"SELECT {str(self.data_list).translate(table)} FROM wunderground WHERE date > '{first_date}' and location='{self.location}' ORDER BY date DESC"
        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()
        #print (self.data)



    def get_current_data(self):
        out_dict = {}
        x = 0
        inc = 0
        print(self.data_list)
        for key in self.data_list:
            print(key)
            #print(self.data[x][inc])
            #print(self.data)
            out_dict[key] = self.data[x][inc]
            #out_dict[key] = self.data[inc]
            inc +=1
            #print (inc)
            #print (out_dict)
        self.current_conditions = out_dict
        #print (out_dict)

    def return_value_list(self, data, name):
        """data is data list, name is key of wanted value"""
        out_dict = {}
        inc = 0
        for key in self.data_list:
            out_dict[key] = data[inc]
            inc +=1
        return out_dict[name]



    def get_last_dates(self):
        """ can only be called after get_data has been called. 
        This method will then go through all the data and get the last entry from each day"""
        sql =  "SELECT date FROM wunderground ORDER BY date ASC"
        self.cursor.execute(sql)
        dates = self.cursor.fetchall()
        out_dates = []
        self.last_time_of_day_list = []
        last_day = dates[0][0].date()
        last_time = dates[0][0].time()
        possible_day = ''
        for date in dates:
            if date[0].date() == last_day:
                if date[0].time() > last_time:
                    last_time = date[0].time()
                    possible_day = date[0]
                    #last_time_of_day_list.append(date[0])
            elif date[0].date() > last_day:
                self.last_time_of_day_list.append(possible_day)
                # this won't collect data from a day if there is only one entry from that day
                last_day =  date[0].date()
                last_time = date[0].time()

            if date[0].date() < last_day:
                pass

            out_dates.append(date[0])
            # TESTING
            #print (self.last_time_of_day_list)
        #for date in self.last_time_of_day_list:
        #    print (date)

    def return_daily_precip(self, date):
        """Only call after get_last_dates.
        This method will get the today_precip from each of those entries"""
        #for date in self.last_time_of_day_list:
        for entry in self.data:
            if date in entry:
                #TESTING
                #print (self.return_value_list(entry))
                return (self.return_value_list(entry, 'today_precip'))

    def get_weekly_precip(self):
        """should this always return info for the last week, or should it take a day as input?"""
        #changing to list of tuples to keep order
        #self.total_dict = {}
        self.total_list = []
        self.weekly_precip = 0
        for date in self.last_time_of_day_list[-7:]:
            if date != '':
                self.total_list.append(tuple((date, self.return_daily_precip(date))))
                #self.total_dict[date] = self.return_daily_precip(date)

        try:
            for day in self.total_list:
                if day[1] != None:
                    self.weekly_precip += day[1]
        except TypeError as error:
            #raise error
            pass


    def get_yearly_precip(self):
        pass

    def get_pressure_direction(self):
        out_list = []
        for entry in self.data[:7]:

            #pressure = self.return_value_list(entry, 'current_pressure')
            out_list.append(entry[2])
        out_list.reverse()
        return out_list

    def get_point_list(self):
        pressure_list = self.get_pressure_direction()
        if len(pressure_list) < 6:
            out_html = 'No data'
            print( self.location, ': low data')
            return out_html
        if (abs(pressure_list[6]) - abs(pressure_list[5])) > .03 or (abs(pressure_list[6]) - abs(pressure_list[4])) > .02:
            if (pressure_list [6] > pressure_list[5]) or (pressure_list [6] > pressure_list[4]):
                out_var = "10,30 10,0 0,4 20,4, 10,0"
                out_html = '&#8593'
                print (self.location, ': up')
            else:
                out_var = "10,0 10,30, 0,26, 20,26 10,30"
                out_html = '&#8595'
                print (self.location, ': down')
            
        else:
            out_var = "10,0 10,30 0,26 20,26, 10,30"
            out_html = '&#8594'
            print (self.location, ': steady')

        return out_html

        
 


if __name__=="__main__":
    start = time.process_time()
    location_list = ['KWACARNA1', 'KWAFALLC80', 'KWAFALLC81']
    #location_list = ['KWACARNA1', 'KWAFALLC80']
    #location_list = ['KWAFALLC80', 'KWACARNA1' ]
    out_list = []
    for location in location_list:
        weather_data = wunder_data(cnx, location)
        out_list.append(weather_data.template_out_dict())

    forecast_data = wu_forecast(cnx)
    forecast_list = forecast_data.get_out_list()


    #print (out_list)
    output_text = output_template.render_template(out_list, forecast_list)

    with open('/var/www/weather_app/index.html', 'w') as out:
            out.write(output_text)
    end = time.process_time()
    print (end - start)

    
