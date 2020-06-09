import mysql_config
import mysql.connector
from mysql.connector import errorcode
import datetime


cnx = mysql.connector.connect(**mysql_config.config)

class wunder_data():
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.get_data()
        self.get_current_data()
        self.get_last_dates()
        self.get_weekly_precip()

    def __str__(self):
        output = ''
        for entry in self.data_list:
            output += entry + ": " + str(self.current_conditions[entry])
            output +='\n'
            #print (entry + " : ")
            #print (self.current_conditions[entry])

        output += ("Total rainfall for this week is : " + str(self.weekly_precip))
        return output


    def get_json(self):
        pass

    def get_data(self):
        table = {39: None, 91: None, 93: None}
        self.data_list = ['date', 'current_pressure', 'current_temp', 'today_precip', 'current_humidity']
        sql = "SELECT {} FROM wunderground ORDER BY date DESC".format(str(self.data_list).translate(table))
        #print(sql)
        self.cursor.execute(sql)
        self.data = self.cursor.fetchall()



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

            
            #print (date[0].date())
            #print (date[0])
            out_dates.append(date[0])
        #for date in self.last_time_of_day_list:
        #    print (date)

    def return_daily_precip(self, date):
        """Only call after get_last_dates.
        This method will get the today_precip from each of those entries"""
        #for date in self.last_time_of_day_list:
        for entry in self.data:
            if date in entry:
                return (self.return_precip(entry))

    def get_weekly_precip(self):
        """should this always return info for the last week, or should it take a day as input?"""
        total_dict = {}
        self.weekly_precip = 0
        for date in self.last_time_of_day_list[-7:]:
            total_dict[date] = self.return_daily_precip(date)

        for day in total_dict:
            self.weekly_precip += total_dict[day]








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

test = wunder_data(cnx)
print (test)
#test.get_data()
#test.print_current_data()
#test.get_last_dates()
#test.get_weekly_precip()


