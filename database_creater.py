import mysql.connector
from mysql.connector import errorcode
import mysql_config


def create_table(TABLE_NAME, TABLE_LIST):
    cnx = mysql.connector.connect(**mysql_config.config)
    cursor = cnx.cursor()
    #cursor.execute ("DROP TABLE {}".format (TABLE_NAME))

    try:
        cursor.execute ("USE {}".format('weather_app'))
    except mysql.connector.Error as err:
        print ("Database {} does not exist.".format('weather_app'))
        raise err

    try:
        cursor.execute('CREATE TABLE ' + TABLE_NAME + ' (' + TABLE_LIST[0] + ')')
        print ('Created table {}.'.format(TABLE_NAME))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print ('table was already created')


    for column in TABLE_LIST:
        try:
            print ("Adding column ", column)
            cursor.execute('ALTER TABLE ' + TABLE_NAME + ' ADD ' + column)
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print ("column already existed")

    cursor.close()
    cnx.close()


def create_wunderground_table():

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
    #cursor.execute ("DROP TABLE {}".format (TABLE_NAME))

    try:
        cursor.execute ("USE {}".format('weather_app'))
    except mysql.connector.Error as err:
        print ("Database {} does not exist.".format('weather_app'))
        raise err

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

    cursor.close()
    cnx.close()


def create_accuweather_table():
    TABLE_NAME = 'accuweather'
    TABLE_LIST = ['date datetime',
            'hour_precip decimal(6,2)',
            'humidity decimal(6,2)',
            'temperature decimal(6,2)',
            '12_hour_precip decimal(6,2)',
            '24_hour_precip decimal(6,2)',
            'pressure decimal(6,2)',
            'pressure_tendancy VARCHAR(255)',
            'apparent_temperature decimal(6,2)',
            'indoor_relative_humidity decimal(6,2)',
            'feels_like_temperature decimal(6,2)',
            'relative_humidity decimal(6,2)',
            'wet_bulb_temperature decimal(6,2)',
            'wind_direction decimal(6,2)',
            'wind_speed decimal(6,2)',
            'dew_point decimal(6,2)',
            'temperature_max_past_12 decimal(6,2)',
            'temperature_min_past_12 decimal(6,2)',
            'temperature_max_past_24 decimal(6,2)',
            'temperature_min_past_24 decimal(6,2)'



            ]
    cnx = mysql.connector.connect(**mysql_config.config)
    cursor = cnx.cursor()
    cursor.execute ("DROP TABLE {}".format (TABLE_NAME))

    try:
        cursor.execute ("USE {}".format('weather_app'))
    except mysql.connector.Error as err:
        print ("Database {} does not exist.".format('weather_app'))
        raise err

    try:
        print ('creating table ', TABLE_NAME)
        cursor.execute('CREATE TABLE ' + TABLE_NAME + ' (' + TABLE_LIST[0] + ')')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print ('table was already created')
    
    for column in TABLE_LIST:
        try:
            print ("Adding column ", column)
            cursor.execute('ALTER TABLE ' + TABLE_NAME + ' ADD ' + column)
        except mysql.connector.Error as err:
            if err.errno == 1060:
                print ("Column already existed")
            else: raise err

    cursor.close()
    cnx.close()

wunderground_column_list = [
        'date datetime',
        'location VARCHAR(255)',
        'current_pressure decimal(6,2)',
        'current_temp decimal(6,2)',
        'today_precip decimal(6,2)',
        'current_humidity decimal(6,2)',
        'wind_speed decimal(6,2)',
        'wind_direction decimal(6,2)',
        'wind_gust decimal(6,2)',
        'wind_chill decimal(6,2)',
        'dew_point decimal(6,2)'
        ]

wunderground_forecast_column_list = [
        'date_gathered datetime',
        'date_forecast datetime',
        'max_temp decimal(6,2)',
        'min_temp decimal(6,2)',
        'qpf decimal(6,2)',
        'precip_type_day VARCHAR(255)',
        'precip_type_night VARCHAR(255)',
        'precip_chance_day decimal(6,2)',
        'precip_chance_night decimal(6,2)',
        'relative_humidity_day decimal(6,2)',
        'relative_humidity_night decimal(6,2)',
        'wx_phrase_day VARCHAR(255)',
        'wx_phrase_night VARCHAR(255)',
        'snow_amount_day decimal(6,2)',
        'snow_amount_night decimal(6,2)',
        'wind_direction_day decimal(6,2)',
        'wind_direction_night decimal(6,2)',
        'wind_direction_cardinal_day VARCHAR(255)',
        'wind_direction_cardinal_night VARCHAR(255)',
        'wind_speed_day decimal(6,2)',
        'wind_speed_night decimal(6,2)',
        'cloud_cover_chance_day decimal(6,2)',
        'cloud_cover_chance_night decimal(6,2)'
        ]



accuweather_column_list = [
        'date datetime',
        'location VARCHAR(255)',
        'hour_precip decimal(6,2)',
        'humidity decimal(6,2)',
        'temperature decimal(6,2)',
        '12_hour_precip decimal(6,2)',
        '24_hour_precip decimal(6,2)',
        'pressure decimal(6,2)',
        'pressure_tendancy VARCHAR(255)',
        'apparent_temperature decimal(6,2)',
        'indoor_relative_humidity decimal(6,2)',
        'feels_like_temperature decimal(6,2)',
        'relative_humidity decimal(6,2)',
        'wet_bulb_temperature decimal(6,2)',
        'wind_direction decimal(6,2)',
        'wind_speed decimal(6,2)',
        'dew_point decimal(6,2)',
        'temperature_max_past_12 decimal(6,2)',
        'temperature_min_past_12 decimal(6,2)',
        'temperature_max_past_24 decimal(6,2)',
        'temperature_min_past_24 decimal(6,2)'
        ]

create_table('wunderground', wunderground_column_list)
#create_table('accuweather', accuweather_column_list)
#create_table('wunderground_forecast', wunderground_forecast_column_list)
