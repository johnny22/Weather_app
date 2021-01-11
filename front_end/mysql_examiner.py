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
        self.get_data()
        self.get_current_data()


    def __str__(self):
        one = False



        if one:
            output = ''
            for entry in self.data_list:
                output += entry + ": " + str(self.current_conditions[entry])
                output +='\n'
                #print (entry + " : ")
                #print (self.current_conditions[entry])
                print ('we are not here, right?')
            return output
        else:
            output = ''
            for line in self.data:
                #print (line)
                for entry in self.data_list:
                    output += entry + ": " + str(line[self.data_list.index(entry)])
                    output += '     '
                output +='\n'
            return output

    def get_data(self):
        table = {39: None, 91: None, 93: None}
        self.data_list = ['location', 'date', 'current_pressure', 'current_temp', 'today_precip', 'current_humidity']
        sql = "SELECT {} FROM wunderground ORDER BY date DESC".format(str(self.data_list).translate(table))
        print(sql)
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




out = examiner(cnx)
print (out)
