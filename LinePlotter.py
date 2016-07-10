# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LinePlotter
                                 A QGIS plugin
 Plot line shapes from .csv files
                              -------------------
        begin                : 2016-03-16
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Andres Arguello & Abdenago Guzman / UCR
        email                : aarguello@eie.ucr.ac.cr & nagoguzle@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from LinePlotter_dialog import LinePlotterDialog
import os.path
from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *
import csv
#Para desplegar mensajes, útil para debugin
import sys
import numpy as np

class LinePlotter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LinePlotter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = LinePlotterDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&LinePlotter')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LinePlotter')
        self.toolbar.setObjectName(u'LinePlotter')
        self.dlg.pushButton.clicked.connect(self.select_output_folder)
        self.dlg.pushButton_run.clicked.connect(self.run_code)
	
    def select_output_folder(self):
        """Método para seleccionar la carpeta de destino"""
        filename = QFileDialog.getOpenFileName(self.dlg, QCoreApplication.translate('dialog', "Seleccione el archivo.csv con las coordenadas"), "",)
        self.dlg.lineEdit_dirOutput.setText(filename)
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LinePlotter', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/LinePlotter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'LinePlotter'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&LinePlotter'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        self.dlg.show()
        result = self.dlg.exec_()

   
    def run_code(self):
        filename = self.dlg.lineEdit_dirOutput.text()
        name = self.dlg.lineEdit_dirOutput_2.text().upper()
        X1 = self.dlg.lineEdit_X1.text().upper() 
        Y1 = self.dlg.lineEdit_Y1.text().upper() 
        X2 = self.dlg.lineEdit_X2.text().upper() 
        Y2 = self.dlg.lineEdit_Y2.text().upper() 
        if not X1:
            X1 = '6'
        else:
            X1 = self.dlg.lineEdit_X1.text()
        if not Y1:
            Y1 = '7'
        else:
            Y1 = self.dlg.lineEdit_Y1.text()
        if not X2:
            X2 = '8'
        else:
            X2 = self.dlg.lineEdit_X2.text()
        if not Y2:
            Y2 = '9'				
        else:
            Y2 = self.dlg.lineEdit_Y2.text()
        if not name:
            name = 'Generic_line_layer_name'
        else:
            name = self.dlg.lineEdit_dirOutput_2.text()
        if filename:                
            workbook = open(filename,'rt')
            reader = csv.reader(workbook)
            col=next(reader)
            Data_X_Y = [[row[int(X1)-1],row[int(Y1)-1],row[int(X2)-1],row[int(Y2)-1]] for row in reader]
			
            Data = []
            with open(filename, 'r') as f:
                for line in f.readlines():
                    l = line.split(',')
                    Data.append(l)	
			
        layer =  QgsVectorLayer('LineString', name , "memory")
        pr = layer.dataProvider()
				
        for ij in range(len(Data_X_Y)):
            x1_p=float(Data_X_Y[ij][0])
            y1_p=float(Data_X_Y[ij][1])
            x2_p=float(Data_X_Y[ij][2])
            y2_p=float(Data_X_Y[ij][3])
            point1 = QgsPoint(x1_p,y1_p)
            point2 = QgsPoint(x2_p,y2_p)
            line = QgsFeature()
            line.setGeometry(QgsGeometry.fromPolyline([point1,point2]))
            pr.addFeatures([line])	
            layer.updateExtents()
            layer.updateFields()
            QgsMapLayerRegistry.instance().addMapLayers([layer])
			
        for ik in range(len(col)):
            pr.addAttributes([QgsField(str(col[ik]), QVariant.String)])

        iF = layer.getFeatures()
        layer.startEditing()
        for feat in iF:
            for ik in range(len(col)):
                layer.changeAttributeValue(feat.id(), ik, Data[feat.id()][ik])
        layer.commitChanges()
		
		
		