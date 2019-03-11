#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import datetime
from agent_manager_sql import AgentDataStore

class AgentManagerAddNew(QtWidgets.QDialog):
    
    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.output = dict()
        self.agent_data = AgentDataStore()
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
        self.siteCombo = QtWidgets.QComboBox()
        self.titleCombo = QtWidgets.QComboBox()
        self.firstnameEdit = QtWidgets.QLineEdit()
        self.surnameEdit = QtWidgets.QLineEdit()
        #display name edit?
        self.tntloginEdit = QtWidgets.QLineEdit()
        self.avayanameEdit = QtWidgets.QLineEdit()
        self.extensionEdit = QtWidgets.QLineEdit()
        self.loginnumberEdit = QtWidgets.QLineEdit()
        self.startdateEdit = QtWidgets.QDateEdit()
        
        self.extensionEdit.setInputMask("000000")
        self.loginnumberEdit.setInputMask("00000")
        #self.siteCombo.addItems(("UK","SA","Other"))
        #self.titleCombo.addItems(("Agent","Senior Agent","Team Leader","Other"))
        self.startdateEdit.setDate(datetime.today())
        
        fboxForm.addRow("First name", self.firstnameEdit)
        fboxForm.addRow("Surname", self.surnameEdit)
        fboxForm.addRow("Site", self.siteCombo)
        fboxForm.addRow("Title", self.titleCombo)
        fboxForm.addRow("TnT login", self.tntloginEdit)
        fboxForm.addRow("Avaya name", self.avayanameEdit)
        fboxForm.addRow("Agent extension", self.extensionEdit)
        fboxForm.addRow("Phone login", self.loginnumberEdit)
        fboxForm.addRow("Start date", self.startdateEdit)
        #agent extension edit int
        #avaya extension edit int

        hbox_main_panel.addLayout(fboxForm)
        hbox_main_panel.addLayout(vbox_button_panel)
        self.setWindowTitle('Add new agent')

        self.siteCombo.addItems(self.agent_data.site_values())
        self.titleCombo.addItems(self.agent_data.title_values())
        
        save_button.clicked.connect(self.call_save)
        cancel_button.clicked.connect(self.call_cancel)
    
    def call_save(self):
        self.output['surname'] = self.surnameEdit.text()
        self.output['firstname'] = self.firstnameEdit.text()
        self.output['tnt'] = self.tntloginEdit.text()
        self.output['avaya'] = self.avayanameEdit.text()
        self.output['extension'] = self.extensionEdit.text()
        self.output['login'] = self.loginnumberEdit.text()
        self.output['startdate'] = self.startdateEdit.text()
        self.output['site'] = self.siteCombo.currentText()
        self.output['title'] = self.titleCombo.currentText()
        self.accept()
    
    def call_cancel(self):
        self.reject()

    @staticmethod
    def getAgentDetails(parent = None):
        dialog = AgentManagerAddNew(parent)
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Accepted:
            return_result = dict()
            return_result = dialog.output
            return (return_result, True)
        else:
            return (dict(), False)
        #return ("Hello", result == QtWidgets.QDialog.Accepted)