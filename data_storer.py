import datetime
import mysql.connector
from mysql.connector import errorcode
import mysql_config


cnx = mysql.connector.connect(**mysql_config.config)
cursor = cnx.cursor()

def unpack(s):
    return " ".join(map(str, s))

def store_data(table, column, data):
    sql = "INSERT INTO %s %s VALUE %s" % (table, column, data)
    try:
        print (sql)
        cursor.execute(sql)
        cnx.commit()
    except ValueError:
        print('bummer')

    #print (table, column, data)


def store_list(table, data_dict):
    current_date = str(datetime.datetime.now())[:-4]
    #print ('here')
    #print (current_date)
    data_dict['date'] ="'" +  str(current_date) + "'"

    #print (data_dict)



    column_list = []
    for column in data_dict:
        column_list.append(column)
    column_list = tuple(column_list)

    data_list = [data_dict[column] for column in column_list]
    data_list = tuple(data_list)
    
    #print ("columns", column_list)
    #print (data_list)
    translation = {39: None}
    sql = "INSERT INTO {} ".format(table) + "{} ".format(str(column_list).translate(translation))
    sql += " VALUES" + "{} ".format(str(data_list).translate(translation))
    #sql = f."INSERT INTO {table} ({unpack(column_list)}) VALUES ({unpack(data_list)})"
    #sql = "INSERT INTO {} ({}) VALUES ({})".format(table, *column_list, *data_list)
    try:
        #sql = "INSERT INTO wunderground (current_temp, current_pressure, today_precip, current_humidity, date) VALUES(25,59,.3,65, '{}')".format(current_date)
        #print (sql)
        cursor.execute(sql)
        cnx.commit()
    except ValueError:
        print('bummer')
    #for column in data_dict:
    #    store_data(table, column, data_dict[column])




if __name__ == "__main__":
    test_dict = {
            'current_temp' : '25',
            'current_pressure' : 59,
            'today_precip' : .3,
            'current_humidity' : 65
            }
    store_list('wunderground', test_dict)



