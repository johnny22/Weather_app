import mysql.connector
from mysql.connector import errorcode
import mysql_config


TABLE_NAME = 'wunderground'
ACTION_VAR = 'CREATE TABLE'
TABLE_LIST = [
        'date datetime',
        'current_pressure decimal(6,2)',
        'current_temp decimal(6,2)',
        'today_precip decimal(6,2)',
        'current_humidity decimal(6,2)'
        ]


        


cnx = mysql.connector.connect(**mysql_config.config)
cursor = cnx.cursor()
cursor.execute ("DROP TABLE {}".format (TABLE_NAME))

try:
    cursor.execute ("USE {}".format('weather_app'))
except mysql.connector.Error as err:
    print ("Database {} does not exist.".format('weather_app'))
    print (err)
#cursor.execute("CREATE TABLE wunderground (date DATETIME, current_pressure DECIMAL)") 

try:
    cursor.execute(ACTION_VAR + ' ' + TABLE_NAME + ' (' + TABLE_LIST[0] + ')')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print ('table was already created')


for column in TABLE_LIST:
    try:
        cursor.execute('ALTER TABLE ' + TABLE_NAME + ' ADD ' + column)
    except mysql.connector.Error as err:
        if err.errno == 1060:
            print ("column already existed")

#for table_name in CREATE_TABLES:
#    table_description = CREATE_TABLES[table_name]
#    try:
#        print ("Creating table {}: ".format(table_name))
#        print (table_description)
#        cursor.execute(table_description)
#    except mysql.connector.Error as err:
#        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#            print("table already created, let's try altering instead")
#            try:
#                print ('what about now?')
#                print  (ALTER_TABLES['wunderground'])
#                cursor.execute(ALTER_TABLES['wunderground'])
#                print ('do we get here?')
#            except mysql.connector.Error as err1:
#                print ('so we are here?')
#                print (err1)
#        else:
#            print ("we are trying to create the table")
#            print (err)


cursor.close()
cnx.close()
