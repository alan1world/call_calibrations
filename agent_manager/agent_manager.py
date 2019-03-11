#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore
#from datetime import datetime
import sys

from agent_manager_new import AgentManagerAddNew
from agent_manager_sql import AgentDataStore

class AgentManagerMain(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.agent_data = AgentDataStore()
        self.initUI()

    def initUI(self):

        vbox_main_panel = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()

        hbox_top_panel = QtWidgets.QHBoxLayout()

        vbox_button_panel = QtWidgets.QVBoxLayout()
        save_button = QtWidgets.QPushButton('Save', self)
        cancel_button = QtWidgets.QPushButton('Cancel', self)
        addnew_button = QtWidgets.QPushButton('Add New', self)
        vbox_button_panel.addWidget(save_button)
        vbox_button_panel.addWidget(cancel_button)
        vbox_button_panel.addWidget(addnew_button)

        filter_panel = QtWidgets.QGridLayout()
        team_filter_label = QtWidgets.QLabel("Team:")
        status_filter_label = QtWidgets.QLabel("Status:")
        uk_filter_button = QtWidgets.QPushButton('UK', self)
        sa_filter_button = QtWidgets.QPushButton('SA', self)
        other_filter_button = QtWidgets.QPushButton('Other', self)
        active_filter_button = QtWidgets.QPushButton('Active', self)
        inactive_filter_button = QtWidgets.QPushButton('Inactive', self)
        uk_filter_button.setCheckable(True)
        sa_filter_button.setCheckable(True)
        other_filter_button.setCheckable(True)
        active_filter_button.setCheckable(True)
        inactive_filter_button.setCheckable(True)
        uk_filter_button.setChecked(True)
        sa_filter_button.setChecked(True)
        active_filter_button.setChecked(True)
        filter_panel.addWidget(team_filter_label,0,0)
        filter_panel.addWidget(status_filter_label,1,0)
        filter_panel.addWidget(uk_filter_button,0,1)
        filter_panel.addWidget(sa_filter_button,0,2)
        filter_panel.addWidget(other_filter_button,0,3)
        filter_panel.addWidget(active_filter_button,1,1)
        filter_panel.addWidget(inactive_filter_button,1,2)
        
        self.tableView = QtWidgets.QTableView()
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        spacer = QtWidgets.QSpacerItem(100,10)
        #table_header = QtWidgets.QHeaderView()

        
        hbox_top_panel.addLayout(filter_panel)
        hbox_top_panel.addItem(spacer)
        hbox_top_panel.addLayout(vbox_button_panel)
        vbox_main_panel.addLayout(hbox_top_panel)
        vbox_main_panel.addWidget(self.tableView)
        widget.setLayout(vbox_main_panel)
        self.setCentralWidget(widget)
        self.setWindowTitle('Agent Manager')

        addnew_button.clicked.connect(self.call_add_new_agent)
        save_button.clicked.connect(self.call_save)
        cancel_button.clicked.connect(self.call_cancel)

        self.agentModel = QtGui.QStandardItemModel()
        self.agentModel.setHorizontalHeaderLabels(('Name','Status','Title','Site'))
        self.update_table()
    
    def call_add_new_agent(self):

        self.hide()
        new_agent = []
        new_agent = AgentManagerAddNew.getAgentDetails()
        self.show()
        print(new_agent)

    def call_save(self):
        self.close()

    def call_cancel(self):
        self.close()

    def update_table(self):
        input_list = self.agent_data.agent_values()
        for row in input_list:
            row_list = []
            for item in row:
                row_list.append(QtGui.QStandardItem(item))
            self.agentModel.appendRow(row_list)
        self.tableView.setModel(self.agentModel)

def main():
    app = QtWidgets.QApplication([])

    win = AgentManagerMain()
    #win = AgentManagerAddNew()
    win.show()
    #win.raise_()
    app.exec_()

if __name__ == "__main__":
    main()