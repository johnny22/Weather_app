import mysql_config
import mysql.connector
from mysql.connector import errorcode


cnx = mysql.connector.connect(**mysql_config.config)

class wunder_data():
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def get_json(self):
        pass

    def print_data(self):
        table = {39: None, 91: None, 93: None}
        data_list = ['date', 'current_pressure', 'current_temp', 'today_precip', 'current_humidity']
        sql = "SELECT {} FROM wunderground ORDER BY date DESC".format(str(data_list).translate(table))
        #print(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        out_dict = {}
        rows = len(data)
        x = 0
        inc = 0
        for key in data_list:
            out_dict[key] = data[x][inc]
            inc +=1
            #print (inc)
            #print (out_dict)
        print (out_dict)



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

test.print_data()

