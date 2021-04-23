import sys

from data.business import find_business
from data.distance import lonlat_distance
from data.geocoder import get_coordinates
from data.mapapi_PG import show_map

toponym_to_find = " ".join(sys.argv[1:])

if toponym_to_find:
    toponym_lattitude, toponym_longitude = get_coordinates(toponym_to_find)
    address_ll = f"{toponym_lattitude},{toponym_longitude}"
    delta = "0.005"
    spn = ",".join([delta, delta])

    # Получаем координаты ближайшей аптеки.
    organization = find_business(address_ll, spn, "аптека")
    # Название организации.
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    # Время работы организации.
    org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]

    # Получаем координаты ответа.
    point = organization["geometry"]["coordinates"]
    org_lat, org_lon = float(point[0]), float(point[1])
    point_param = f"pt={org_lat},{org_lon},pm2dgl"

    # Добавляем на карту точку с исходным адресом.
    point_param = point_param + f"~{address_ll},pm2rdl"

    show_map(map_type="map", add_params=point_param)

    # Расстояние до организации.
    distance = round(lonlat_distance((toponym_longitude, toponym_lattitude),
                                     (org_lon, org_lat)))

    snippet = f"Адрес:\t{org_address}\n" \
              f"Название:\t{org_name}\n" \
              f"Время работы:\t{org_time}\n" \
              f"Расстояние:\t{distance} м"
    print(snippet)
