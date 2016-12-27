import math
# encoding: UTF-8

EARTH_RADIUS = 6378.137

def getPointDistance(lat1, lng1, lat2, lng2):
    result = 0

    radLat1 = radian(lat1)

    radLat2 = radian(lat2)

    a = radian(lat1) - radian(lat2)

    b = radian(lng1) - radian(lng2)

    result = 2*math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                   math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)));
    result = result * EARTH_RADIUS
    result = round(result * 1000) / 1000.0
    return result

def radian(d):
    return (d * math.pi) / 180.00
