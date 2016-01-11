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
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from npcompdec import DecMap


def plotWorldDec(coords, res, bbox):

    fig=plt.figure(figsize=(20,12))
    ax = fig.add_axes([0.1,0.1,0.75,0.75])


    #m = Basemap(llcrnrlon=-180,llcrnrlat=-85,urcrnrlon=180,urcrnrlat=85,projection='mill')
    m = Basemap(llcrnrlon=bbox[3],llcrnrlat=bbox[2],urcrnrlon=bbox[1],urcrnrlat=bbox[0],projection='mill')

    lat, lon = coords
    x,y = m(lon, lat)

    ct_range = range(-200, 201, 2)
    cs = m.contour(x,y,res,ct_range,cmap=plt.cm.jet)
    #cs = m.contour(x,y,res,ct_range,cmap=plt.cm.coolwarm)
    #cs = m.contour(x,y,res,ct_range,colors="b")
    plt.clabel(cs, inline=1, fmt='%1i', fontsize=10)

    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.drawmeridians(np.arange(0,360,30),labels=[0,0,0,1])
    m.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
    # new axis for colorbar.
    cax = plt.axes([0.875, 0.10, 0.03, 0.75])
    plt.colorbar(cs, cax, format='%g') # draw colorbar
    plt.axes(ax)  # make the original axes current again
    plt.title("Declination World Map", fontsize=12)

    plt.show()

def main():
    #(Maximum latitude, Maximum Longitude, lat_min, lon_min)
    bbox = (85., 180., -85., -180.)
    prec = 2 # 2 degrees of precision
    decmap = DecMap()
    coords, res = decmap.build(bbox, prec)

    plotWorldDec(coords, res, bbox)

if __name__ == '__main__':
  main()
