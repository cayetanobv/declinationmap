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
from osgeo import gdal
from npcompdec import DecMap


def getDec(bbox, prec=1):
    """
    Getting declinations...
    """
    decmap = DecMap()
    coords, dec_data = decmap.build(bbox, prec)

    return(coords, dec_data)

def getGeotransform(bbox, prec):
    """
    Getting geotransformation (affine transform) from array data

    """
    spat_res = 1. / prec
    return(bbox[3], spat_res, 0, bbox[0], 0, spat_res * -1)

def buildRasterLayer(data, geotransform, dst_filepath):
    """
    Building raster data
    """
    cols, rows = data.shape

    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(dst_filepath, rows, cols, 1, gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)
    band = dst_ds.GetRasterBand(1)
    band.WriteArray(data)

    dst_ds=None

def main():
    #(Maximum latitude, Maximum Longitude, lat_min, lon_min)
    bbox = (85., 180., -85., -180.)
    prec = 2 # precision

    coords, dec_data = getDec(bbox, prec)
    # print dec_data

    geotr = getGeotransform(bbox, prec)

    out_raster = "/tmp/dec.tif"
    buildRasterLayer(dec_data.T, geotr, out_raster)

if __name__ == '__main__':
  main()
