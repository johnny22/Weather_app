from ambient_api.ambientapi import AmbientAPI
import time

AMBIENT_ENDPOINT="https://api.ambientweather.net/v1"
AMBIENT_API_KEY='8f50cfbcc72e421b9cce87bd28f051fc56d6a85cf31e4bc8bc746912bd080fa8'
AMBIENT_APPLICATION_KEY='ded210ad609a4cdcb77f734956f89d06d5393923d94d4210a83c736667f4e304'

api = AmbientAPI()

devices = api.get_devices()
print (devices)

#device = devices[0]
#
#print (device.get_data())
