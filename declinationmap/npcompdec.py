# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015-2016.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


import numpy as np
import geomag


class NpCompDec(object):
    """
    Data from World Magnetic Model:
    http://www.ngdc.noaa.gov/geomag/WMM/DoDWMM.shtml
    """

    def __genLatLon(self, bbox, prec):
        """
        """

        lat_max, lon_max, lat_min, lon_min = bbox

        lat = np.linspace(lat_max, lat_min, (abs(lat_min - lat_max) * prec) + 1)
        lon = np.linspace(lon_min, lon_max, (abs(lon_min - lon_max) * prec) + 1)

        return np.meshgrid(lat, lon, sparse=False, indexing='xy')


    def __magDec(self, gm, lat, lon, time):
        """
        """
        if time:
            mag = gm.GeoMag(lat,lon, time=time)
        else:
            mag = gm.GeoMag(lat,lon)

        return mag.dec


    def build(self, bbox, sp_rst, time, wmmfl="data/WMM.COF"):
        """
        """
        coords = self.__genLatLon(bbox, sp_rst)

        lat, lon = coords

        gm = geomag.geomag.GeoMag(wmmfl)

        vectMagDec = np.vectorize(self.__magDec)
        res = vectMagDec(gm, lat, lon, time)

        return(coords, res)
