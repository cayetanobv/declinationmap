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

from datetime import date
from decmap import DecMap


def runTestBbox():

    out_vector = "/tmp/decmaps_testbbox/dec_contours_bbox.shp"
    out_raster = "/tmp/decmaps_testbbox/dec_bbox.tif"

    #(Maximum latitude, Maximum Longitude, Minimum latitude, Minimum longitude)
    bbox = (60., 20., 30, -20.)
    sp_rst = 2
    time = date(2018, 1, 1)

    decmap = DecMap(bbox, sp_rst)
    decmap.build(out_raster, out_vector, time=time, ct_itv=1)

def runTestWorld():

    out_vector = "/tmp/decmaps_testworld/dec_contours_world.shp"
    out_raster = "/tmp/decmaps_testworld/dec_world.tif"

    #(Maximum latitude, Maximum Longitude, Minimum latitude, Minimum longitude)
    bbox = (85., 180., -85., -180.)
    sp_rst = 1

    decmap = DecMap(bbox, sp_rst)
    decmap.build(out_raster, out_vector, ct_itv=2)

if __name__ == '__main__':
    print("Running test 1...")
    runTestBbox()
    print("Finished test 1...")
    print("Running test 2...")
    runTestWorld()
    print("Finished test 2...")
