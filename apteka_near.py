from io import BytesIO
from PIL import Image
import requests
import sys
from apteka_near_func import get_spn, lonlat_distance

# toponym_to_find = "Улица Ярцевская 27к1"
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
#print(toponym)
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

map_params_biz = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "text": 'аптека ' + toponym_to_find,
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "type": "biz",
    "lang": "ru_RU",
    "format": "json"
}
map_api_server_biz ="https://search-maps.yandex.ru/v1/"
response_biz = requests.get(map_api_server_biz, params=map_params_biz)
json_response_biz = response_biz.json()
toponym_byz = json_response_biz['features'][0]
#print(toponym_byz)
toponym_coodrinates_byz = [str(i) for i in toponym_byz['geometry']['coordinates']]
str1 = ",".join([toponym_longitude, toponym_lattitude, "pm2rdm1"])
str2 =",".join(toponym_coodrinates_byz+["pm2rdm2"])
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(get_spn(toponym)),
    "l": "map",
    "pt":str1 + "~"+str2
}

response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()

snippet = {
    "Название": toponym_byz['properties']['CompanyMetaData']['name'],
    "Адрес": toponym_byz['properties']['CompanyMetaData']['address'],
    "Режим работы":  toponym_byz['properties']['CompanyMetaData']['Hours']['text'],
    "Расстояние до аптеки, м": round(lonlat_distance(toponym_coodrinates, toponym_byz['geometry']['coordinates']),2)
}
print('**** Ближайшая аптека **** ')
for key,value in snippet.items():
    print(key, ': ', value)
