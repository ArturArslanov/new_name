import sys

from pprint import pprint
import requests
from funcs3 import find_apteka, find_spn, lonlat_distance, find_10_aptek
import pygame
import os

if __name__ == '__main__':
    file = 'map.png'

    toponym_to_find = " ".join(sys.argv[1:])
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        raise AttributeError(response.content)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    pt = find_10_aptek(",".join([toponym_longitude, toponym_lattitude]))
    map_params = {
        "l": "map",
        "pt": pt,
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        raise AttributeError(response.content)
    with open(file, mode='wb') as f:
        f.write(response.content)

    pygame.init()
    sprait = pygame.image.load(file)

    size = sprait.get_width(), sprait.get_height()
    screen = pygame.display.set_mode((size))
    screen.blit(sprait, (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(file)
