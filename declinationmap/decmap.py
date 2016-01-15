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

import os
import shutil
import numpy as np
from osgeo import gdal, ogr, osr
from npcompdec import NpCompDec


class DecMap(object):

    def __init__(self, bbox, sp_rst):
        """
        bbox: bounding box
              (
                Maximum latitude,
                Maximum Longitude,
                Minimum latitude,
                Minimum longitude
              )

        sp_rst: spatial resolution
        """
        self.__bbox = bbox
        self.__sp_rst = sp_rst

    def __getDec(self, bbox, time, prec=1):
        """
        Getting declinations...
        """
        npdec = NpCompDec()
        coords, dec_data = npdec.build(bbox, prec, time)

        return(coords, dec_data)

    def __getSpatialRef(self, crs_epsg):
        """
        Getting spatial reference from EPSG code
        """
        sp_ref = osr.SpatialReference()
        sp_ref.ImportFromEPSG(crs_epsg)
        return sp_ref

    def __getGeotransform(self, bbox, prec):
        """
        Getting geotransformation (affine transform) from array data

        """
        spat_res = 1. / prec
        return(bbox[3], spat_res, 0, bbox[0], 0, spat_res * -1)

    def __buildRasterLayer(self, data, geotransform, dst_filepath, crs_epsg=4326):
        """
        Building raster data
        """
        cols, rows = data.shape

        sp_ref = self.__getSpatialRef(crs_epsg)

        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(dst_filepath, rows, cols, 1, gdal.GDT_Float32)

        dst_ds.SetGeoTransform(geotransform)
        dst_ds.SetProjection(sp_ref.ExportToWkt())
        band = dst_ds.GetRasterBand(1)
        band.WriteArray(data)

        dst_ds=None

    def __buildContours(self, raster_flpath, vect_flpath, ct_itv, crs_epsg=4326):
        """
        Building declination contours
        """
        sp_ref = self.__getSpatialRef(crs_epsg)

        vect_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(vect_flpath)
        vect_lyr = vect_ds.CreateLayer(vect_flpath, sp_ref, geom_type=ogr.wkbLineString25D)
        field_defn = ogr.FieldDefn('id', ogr.OFTInteger)
        vect_lyr.CreateField(field_defn)
        field_defn = ogr.FieldDefn('dec', ogr.OFTReal)
        vect_lyr.CreateField(field_defn)

        src_raster = gdal.Open(raster_flpath)
        rst_band = src_raster.GetRasterBand(1)
        gdal.ContourGenerate(rst_band, ct_itv, 0, [], 0, 999999, vect_lyr,0,1)

        vect_ds = None
        src_raster = None

    def __createNewDir(self, dir_path):
        """
        Helper method...
        """
        if os.path.exists(dir_path):
            print "Removed previous folder: {}".format(dir_path)
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
        print "Created new folder: {}".format(dir_path)

    def build(self, out_raster, out_vector, overwrite=True, time=None, ct_itv=4):
        """
        out_raster, out_vector: out filepaths
        ct_itv: contour interval
        """
        if overwrite:
            self.__createNewDir(os.path.dirname(out_raster))
            self.__createNewDir(os.path.dirname(out_vector))

        coords, dec_data = self.__getDec(self.__bbox, time, self.__sp_rst)
        geotr = self.__getGeotransform(self.__bbox, self.__sp_rst)

        self.__buildRasterLayer(dec_data.T, geotr, out_raster)
        self.__buildContours(out_raster, out_vector, ct_itv)
