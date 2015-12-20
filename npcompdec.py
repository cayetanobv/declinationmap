
"""
Data from World Magnetic Model:
http://www.ngdc.noaa.gov/geomag/WMM/DoDWMM.shtml
"""

import numpy as np
import geomag



def __genLatLon(bbox, prec):
    """
    """

    lat_max, lon_max, lat_min, lon_min = bbox

    lat = np.linspace(lat_max, lat_min, (180. * prec) + 1)
    lon = np.linspace(lon_min, lon_max, (360. * prec) + 1)
    
    return np.meshgrid(lat, lon, sparse=False, indexing='xy')


def __magDec(lat, lon, wmmfl):
    """
    """
    gm = geomag.geomag.GeoMag(wmmfl)
    
    mag = gm.GeoMag(lat,lon)
    
    return mag.dec


def run(bbox, prec, wmmfl="data/WMM.COF"):
    """
    """
    coords = __genLatLon(bbox, prec)
    
    lat, lon = coords
    
    vectMagDec = np.vectorize(__magDec)
    res = vectMagDec(lat, lon, wmmfl)
    
    #coords.append(res)
    
    return coords, res




