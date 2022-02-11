from pprint import pprint
from math import radians, cos, sqrt

import requests as req


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = radians((a_lat + b_lat) / 2.)
    lat_lon_factor = cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = sqrt(dx * dx + dy * dy)
    return distance


def quer(name, address=None, results=1):
    quer = "https://search-maps.yandex.ru/v1/"
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    params = {
        "apikey": api_key,
        "text": name,
        "lang": "ru_RU",
        "type": "biz",
        'results': f'{results}'
    }
    if address:
        params['ll'] = address
    return req.get(quer, params=params)


def find_apteka(address):
    response = quer('Аптека', address=address)
    if not response:
        raise AttributeError(response.content)
    res = response.json()
    coords = res['features'][0]['geometry']['coordinates']
    info = res['features'][0]['properties']['CompanyMetaData']
    name = f"название - {info['name']} \naddress: {info['address']}"
    name = f"{name} \nграфик работы: {info['Hours']['text']}"
    return coords, name


def find_spn(toponym):
    response = quer(toponym)
    if not response:
        raise AttributeError(response.content)
    res = response.json()
    coords = res['features'][0]['properties']['boundedBy']
    spn = max(abs(coords[1][0] - coords[0][0]), abs(coords[1][1] - coords[0][1]))
    return spn


def find_10_aptek(address):
    response = quer('Аптека', address=address, results=20)
    if not response:
        raise AttributeError(response.content)
    res = response.json()['features']
    checked = []
    pt = ''
    for i in range(len(res)):
        if len(checked) < 10 and res[i]['properties']['CompanyMetaData']['name'] not in checked:
            checked.append(res[i]['properties']['CompanyMetaData']['name'])
            coords = map(str, res[i]['geometry']['coordinates'])
            text = ',pm'
            try:
                info = res[i]['properties']['CompanyMetaData']['Hours']['Availabilities'][0]
                if 'TwentyFourHours' in dict(info).keys():
                    text += 'gns'
                elif not len(dict(info).keys()):
                    text += 'grs'
                else:
                    text += 'lbs'
            except Exception as ex:
                text += 'grs'
            text += f'{len(checked)}'
            pt += f'{",".join(coords)}{text}'
            if i != len(res) - 1 and len(checked) != 10:
                pt += '~'
    return pt
