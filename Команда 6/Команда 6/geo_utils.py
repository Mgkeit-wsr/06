import geopy
from geopy import distance


def is_point_near(lat1, lon1, lat2, lon2, km=1):
    return geopy.distance.distance(lat1, lon1, lat2, lon2).km <= km


def get_near_polygon(lat, lon, km=1):
    p1 = geopy.distance.distance(kilometers=km).destination((lat, lon), bearing=0)
    p2 = geopy.distance.distance(kilometers=km).destination((lat, lon), bearing=90)
    p3 = geopy.distance.distance(kilometers=km).destination((lat, lon), bearing=180)
    p4 = geopy.distance.distance(kilometers=km).destination((lat, lon), bearing=270)

    lat1 = p1.latitude
    lat2 = p2.latitude
    lat3 = p3.latitude
    lat4 = p4.latitude
    lon1 = p1.longitude
    lon2 = p2.longitude
    lon3 = p3.longitude
    lon4 = p4.longitude

    return (min(lat1, lat2, lat3, lat4), max(lat1, lat2, lat3, lat4)),\
           (min(lon1, lon2, lon3, lon4), max(lon1, lon2, lon3, lon4))
