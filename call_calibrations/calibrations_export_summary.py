#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import itertools

from PyQt5 import QtWidgets, QtGui, QtCore

class CalibrationExportSummary(QtWidgets.QDialog):
    
    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.output = dict()
        self.initUI()

    def initUI(self):
        hbox_main_panel = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_main_panel)

        vbox_button_panel = QtWidgets.QVBoxLayout()
        save_button = QtWidgets.QPushButton('Export', self)
        cancel_button = QtWidgets.QPushButton('Close', self)
        vbox_button_panel.addWidget(save_button)
        vbox_button_panel.addWidget(cancel_button)
        vbox_button_panel.setAlignment(save_button,QtCore.Qt.AlignTop)
        vbox_button_panel.addStretch()

        self.listWidget = QtWidgets.QListWidget()
        years = ('2019', '2018')
        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
                  'Oct', 'Nov', 'Dec')
        #for element in itertools.product('2018','Jan'):
        for year in years:
            for month in months:
                submit = year + ' - ' + month
                self.listWidget.addItem(submit)

        hbox_main_panel.addWidget(self.listWidget)
        hbox_main_panel.addLayout(vbox_button_panel)


    @staticmethod
    def getCalibrationDetails(parent = None):
        dialog = CalibrationExportSummary(parent)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            return_result = dict()
            return_result = dialog.output
            return (return_result, True)
        else:
            return (dict(), False)