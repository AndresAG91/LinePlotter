# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LinePlotter
                                 A QGIS plugin
 Plot line shapes from .csv files
                             -------------------
        begin                : 2016-03-16
        copyright            : (C) 2016 by Andres Arguello & Abdenago Guzman / UCR
        email                : aarguello@eie.ucr.ac.cr & nagoguzle@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load LinePlotter class from file LinePlotter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .LinePlotter import LinePlotter
    return LinePlotter(iface)
