#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from calibrations_sql import CalibrationStore
from functools import partial

class CalibrationAddNew(QtWidgets.QDialog):
    
    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.output = dict()
        self.calibration_data = CalibrationStore()
        self.initUI()

    def initUI(self):
        hbox_main_panel = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_main_panel)

        vbox_button_panel = QtWidgets.QVBoxLayout()
        save_button = QtWidgets.QPushButton('Save', self)
        cancel_button = QtWidgets.QPushButton('Cancel', self)
        vbox_button_panel.addWidget(save_button)
        vbox_button_panel.addWidget(cancel_button)
        vbox_button_panel.setAlignment(save_button,QtCore.Qt.AlignTop)
        vbox_button_panel.addStretch()

        fboxForm = QtWidgets.QFormLayout()
        self.calibrationEdit = QtWidgets.QDateEdit()
        self.agentCombo = QtWidgets.QComboBox()
        self.posCombo = QtWidgets.QComboBox()
        self.flight = QtWidgets.QCheckBox()
        self.hotel = QtWidgets.QCheckBox()
        self.rail = QtWidgets.QCheckBox()
        self.car = QtWidgets.QCheckBox()
        self.score = QtWidgets.QSpinBox()
        self.firstcontact = QtWidgets.QSpinBox()
        self.interactionflow = QtWidgets.QSpinBox()
        self.communication = QtWidgets.QSpinBox()
        self.customerfocus = QtWidgets.QSpinBox()
        self.demeanor = QtWidgets.QSpinBox()
        self.feedback = QtWidgets.QTextEdit()
        #self.feedback = QtWidgets.QPlainTextEdit()
        self.managerreview = QtWidgets.QLineEdit()
        self.reviewedwithmanager = QtWidgets.QLineEdit()
        self.coaching = QtWidgets.QLineEdit()
        self.reviewdate = QtWidgets.QLineEdit()
        self.calibrationEdit.setDate(datetime.today())
        self.agentCombo.setEditable(True)
        self.posCombo.setEditable(True)
        self.score.setRange(0,100)
        self.firstcontact.setRange(0,100)
        self.interactionflow.setRange(0,100)
        self.communication.setRange(0,100)
        self.customerfocus.setRange(0,100)
        self.demeanor.setRange(0,100)

        fboxForm.addRow("Calibration Date", self.calibrationEdit)
        fboxForm.addRow("Agent Name", self.agentCombo)
        fboxForm.addRow("Point of Sale", self.posCombo)
        fboxForm.addRow("Flight", self.flight)
        fboxForm.addRow("Hotel", self.hotel)
        fboxForm.addRow("Rail", self.rail)
        fboxForm.addRow("Car", self.car)
        fboxForm.addRow("Score", self.score)
        fboxForm.addRow("First Contact Resolution", self.firstcontact)
        fboxForm.addRow("Interaction Flow", self.interactionflow)
        fboxForm.addRow("Communication", self.communication)
        fboxForm.addRow("Customer Focus", self.customerfocus)
        fboxForm.addRow("Demeanor", self.demeanor)
        fboxForm.addRow("Feedback", self.feedback)
        fboxForm.addRow("Manager Review", self.managerreview)
        fboxForm.addRow("Reviewed with manager", self.reviewedwithmanager)
        fboxForm.addRow("Coaching", self.coaching)
        fboxForm.addRow("Reviewdate", self.reviewdate)

        hbox_main_panel.addLayout(fboxForm)
        hbox_main_panel.addLayout(vbox_button_panel)
        self.setWindowTitle('New calibration')        

        save_button.clicked.connect(self.call_save)
        cancel_button.clicked.connect(self.call_cancel)

        self.agentCombo.addItems(self.calibration_data.agent_values())
        self.posCombo.addItems(self.calibration_data.pos_values())

        #self.setTabOrder(self.calibrationEdit, self.feedback)
        self.feedback.setTabChangesFocus(True)
        for key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            QtWidgets.QShortcut(key, self, partial(self.focusNextPrevChild, True))

    def call_save(self):
        self.output['date'] = self.calibrationEdit.text()
        self.output['agent'] = self.agentCombo.currentText()
        self.output['pointofsale'] = self.posCombo.currentText()
        self.output['flight'] = self.flight.checkState()
        self.output['hotel'] = self.hotel.checkState()
        self.output['rail'] = self.rail.checkState()
        self.output['car'] = self.car.checkState()
        self.output['score'] = self.score.text()
        self.output['firstcontact'] = self.firstcontact.text()
        self.output['interactionflow'] = self.interactionflow.text()
        self.output['communication'] = self.communication.text()
        self.output['customerfocus'] = self.customerfocus.text()
        self.output['demeanor'] = self.demeanor.text()
        self.output['feedback'] = self.feedback.toPlainText()
        self.output['managerreview'] = self.managerreview.text()
        self.output['reviewedwithmanager'] = self.reviewedwithmanager.text()
        self.output['coaching'] = self.coaching.text()
        self.output['reviewdate'] = self.reviewdate.text()
        if self.agentCombo.currentText() not in self.calibration_data.agent_values():
            self.output['new_agent'] = True
            self.calibration_data.insert_agent(self.agentCombo.currentText())
        else:
            self.output['new_agent'] = False
        if self.posCombo.currentText() not in self.calibration_data.pos_values():
            self.output['new_pos'] = True
            self.calibration_data.insert_pos(self.posCombo.currentText())
        else:
            self.output['new_pos'] = False
        self.accept()

    def call_cancel(self):
        self.reject()
    
    @staticmethod
    def getCalibrationDetails(parent = None):
        dialog = CalibrationAddNew(parent)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            return_result = dict()
            return_result = dialog.output
            return (return_result, True)
        else:
            return (dict(), False)