import sys

from pprint import pprint
import requests
from funcs2 import find_apteka, find_spn, lonlat_distance
import pygame

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

    delta = f"{find_spn(toponym_to_find)}"

    apteka_coords, info = find_apteka(",".join([toponym_longitude, toponym_lattitude]))
    distance = round(lonlat_distance(map(float, apteka_coords), (float(toponym_longitude), float(toponym_lattitude))))
    info = f'{info}\nрасстояние - {distance} m'
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "l": "map",
        "pt": f'{",".join([toponym_longitude, toponym_lattitude])},pmdos1~{",".join(map(str, apteka_coords))},pmgns2',
        'pl': f'{",".join([toponym_longitude, toponym_lattitude])},{",".join(map(str, apteka_coords))}'
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    with open(file, mode='wb') as f:
        f.write(response.content)

    pygame.init()
    sprait = pygame.image.load(file)

    size = sprait.get_width(), sprait.get_height()
    screen = pygame.display.set_mode((size))
    font = pygame.font.Font(None, 20)
    info = info.split('\n')
    screen.blit(sprait, (0, 0))
    for i in range(len(info)):
        text = font.render(info[i], True, (100, 100, 100))
        screen.blit(text, (40, 50+ 20 * i))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
