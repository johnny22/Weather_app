#import wunderground_data_getter as wunder
import wu_current_json as wunder
import accuweather_data_getter as accu
import wu_forecast_getter
import data_storer
import datetime
import time

counter_var = 1

def get_wu_current():
    #get data from wunderground
    ##################################################
    #Need to update from wunderground_data_getter for new way of calling
    #location_list = ['KWACARNA1', 'KWAFALLC80']
    location_list = ['KWACARNA1', 'KWAFALLC80', 'KWAFALLC81']
    page_list = []
    for location in location_list:
        page = wunder.make_call(location)
        if page != None:
            page_list.append((page, location))
    for tup in page_list:
        conditions = wunder.WuData(tup[0], tup[1])
        wunder_data = conditions.out_dict

        #Store wunderground data
        #print (type(wunder_data))
        print(f"Here {wunder_data}")
        data_storer.store_list('wunderground', wunder_data)


def get_accuweather():
    #get data from accuweather
    global counter_var
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
    #location_list = ['47.45%2C-122.31', '47.44%2C-122.30']
    location_list = ['47.45%2C-122.31']
    for loc in location_list:
        forecast_data = wu_forecast_getter.make_call(loc)
        forecast_object = wu_forecast_getter.WuForecast(forecast_data)
        forecast = forecast_object.get_dict_list()
        for day in forecast:
            data_storer.store_list('wunderground_forecast', day)

start = time.process_time()

with open('log.txt', 'a') as log_file:
    #print (datetime.datetime.now())
    log_file.write('\n')
    log_file.write(str(datetime.datetime.now()))

get_wu_current()
get_accuweather()
get_wu_forecast()
end = time.process_time()
print (end - start)
