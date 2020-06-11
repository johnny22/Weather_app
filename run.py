import wunderground_data_getter as wunder
import accuweather_data_getter as accu
import data_storer
import datetime





#get data from wunderground
page = wunder.make_call()
conditions = wunder.WuData(page)
wunder_data = conditions.get_data_dict()

#get data from accuweather
accu_page = accu.make_call()
accu_conditions = accu.AwData(accu_page)
accu_data = accu_conditions.get_data_dict()





#store data
data_storer.store_list('accuweather', accu_data)

data_storer.store_list('wunderground', wunder_data)

with open('log.txt', 'a') as log_file:
    #print (datetime.datetime.now())
    log_file.write('\n')
    log_file.write(str(datetime.datetime.now()))

