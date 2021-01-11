import wunderground_data_getter as wunder
import accuweather_data_getter as accu
import data_storer
import datetime





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

#get data from accuweather
accu_page = accu.make_call()
accu_conditions = accu.AwData(accu_page)
accu_data = accu_conditions.get_data_dict()



#store accuweather data
data_storer.store_list('accuweather', accu_data)


with open('log.txt', 'a') as log_file:
    #print (datetime.datetime.now())
    log_file.write('\n')
    log_file.write(str(datetime.datetime.now()))

