import mysql_config
import mysql.connector
from mysql.connector import errorcode
import datetime
#server only
import os
import output_template


cnx = mysql.connector.connect(**mysql_config.config)

class wunder_data():
    def __init__(self, connection, location):
        self.location = location
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.get_data()
        self.get_current_data()
        self.get_last_dates()
        self.get_weekly_precip()
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


    def get_json(self):
        pass

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

        out_dict['weekly_rain'] = str((self.weekly_precip + out_dict['today_precip']))
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
        self.data_list = ['date', 'location', 'current_pressure', 'current_temp', 'today_precip', 'current_humidity']
        sql = "SELECT {0} FROM wunderground WHERE location='{1}' ORDER BY date DESC".format(str(self.data_list).translate(table), self.location)
        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()
        #print (self.data)



    def get_current_data(self):
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

    def return_precip(self, data):
        out_dict = {}
        inc = 0
        for key in self.data_list:
            out_dict[key] = data[inc]
            inc +=1

        return out_dict['today_precip']


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
                #print (self.return_precip(entry))
                return (self.return_precip(entry))

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
                self.weekly_precip += day[1]
        except TypeError as error:
            pass
        #print (self.total_list)




    def get_monthly_precip(self):
        pass

    def get_yearly_precip(self):
        pass


        """to do:
        select last date of each day and pull data for each of those, then add today_precip"""




        #for x in range(0,rows):
        #    inc = 0
        #    for key in data_list:
        #        out_dict[str(x)+key] = data[x][inc]
        #        inc +=1
        #        #print (inc)
        #        #print (out_dict)
        #print (out_dict)
        #print (type(data))
        #print (data)
location_list = ['KWACARNA1', 'KWAFALLC80']
out_list = []
for location in location_list:
    test = wunder_data(cnx, location)
    out_list.append(test.template_out_dict())


#print (out_list)
output_text = output_template.render_template(out_list)

with open('/var/www/weather_app/index.html', 'w') as out:
        out.write(output_text)

    #test.out_web_file()
#print (test)
#test.get_data()
#test.print_current_data()
#test.get_last_dates()
#test.get_weekly_precip()


