import wunderground_data_getter as wunder
import data_storer
import datetime





#get data
page = wunder.make_call()
conditions = wunder.Wu_Data(page)
wunder_data = conditions.get_data_dict()





#store data


data_storer.store_list('wunderground', wunder_data)

with open('log.txt', 'a') as log_file:
    #print (datetime.datetime.now())
    log_file.write('\n')
    log_file.write(str(datetime.datetime.now()))

