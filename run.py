import wunderground_data_getter as wunder
import accuweather_data_getter as accu
import wu_forecast_getter
import data_storer
import datetime


counter_var = 1

def get_wu_current():
    #get data from wunderground
    ##################################################
    #Need to update from wunderground_data_getter for new way of calling
    location_list = ['KWACARNA1', 'KWAFALLC80']
    page_list = []
    for location in location_list:
        page = wunder.make_call(location)
        page_list.append((page, location))
    for tup in page_list:
        conditions = wunder.WuData(tup[0], tup[1])
        wunder_data = conditions.get_data_dict()

        #Store wunderground data
        data_storer.store_list('wunderground', wunder_data)


def get_accuweather():
    #get data from accuweather
    try:
        with open('counter.txt', 'r+') as counter_file:
            try:
                old_counter = counter_file.read()
                counter_var += int(old_counter)
            except ValueError as e:
                #raise e
                print (e)


            counter_file.truncate(0)
            counter_file.seek(0)
            counter_file.write(str(counter_var))

    except FileNotFoundError:
        with open('counter.txt', 'w') as counter_file:
            counter_file.write(str(1))

    if counter_var % 4 == 0:
        accu_page = accu.make_call()
        accu_conditions = accu.AwData(accu_page)
        accu_data = accu_conditions.get_data_dict()
        #store accuweather data
        data_storer.store_list('accuweather', accu_data)

def get_wu_forecast():
    forecast_data = wu_forecast_getter.make_call('location')
    forecast_object = wu_forecast_getter.WuForecast(forecast_data)
    forecast = forecast_object.get_dict_list()
    print ('storing forecast')
    data_storer.store_list('wunderground_forecast', forecast)



with open('log.txt', 'a') as log_file:
    #print (datetime.datetime.now())
    log_file.write('\n')
    log_file.write(str(datetime.datetime.now()))

#get_wu_current()
#get_accuweather()
get_wu_forecast()
