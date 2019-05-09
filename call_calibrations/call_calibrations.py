#! /usr/bin/env python
#! -*- coding: utf-8 -*-

from datetime import datetime
from statistics import mean, StatisticsError

from PyQt5 import QtWidgets, QtGui, QtCore

from calibrations_sql import CalibrationStore
from calibration_new import CalibrationAddNew
from calibrations_export_summary import CalibrationExportSummary

class CallCalibrationMain(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.calibration = CalibrationStore()
        self.calibration_summary = dict()
        self.store_loc = 0
        self.store_site_value = ""
        self.createActions()
        self.initUI()
        self.createMenus()

    def initUI(self):

        vbox_main_panel = QtWidgets.QVBoxLayout()
        widget = QtWidgets.QWidget()
        hbox_top_panel = QtWidgets.QHBoxLayout()

        vbox_button_panel = QtWidgets.QVBoxLayout()
        save_button = QtWidgets.QPushButton('Update', self)
        cancel_button = QtWidgets.QPushButton('Close', self)
        addnew_button = QtWidgets.QPushButton('New', self)
        vbox_button_panel.addWidget(save_button)
        vbox_button_panel.addWidget(cancel_button)
        vbox_button_panel.addWidget(addnew_button)
        vbox_button_panel.setAlignment(save_button,QtCore.Qt.AlignTop)
        vbox_button_panel.addStretch()

        fboxFilters = QtWidgets.QFormLayout()
        self.agentFilter = QtWidgets.QComboBox()
        self.siteFilter = QtWidgets.QComboBox()
        self.yearFilter = QtWidgets.QComboBox()
        self.monthFilter = QtWidgets.QComboBox()
        #self.weekFilter = QtWidgets.QComboBox()
        self.weekFilter = QtWidgets.QSpinBox()
        fboxFilters.addRow("Agent", self.agentFilter)
        fboxFilters.addRow("Site", self.siteFilter)
        fboxFilters.addRow("Year", self.yearFilter)
        fboxFilters.addRow("Month", self.monthFilter)
        fboxFilters.addRow("Week", self.weekFilter)

        fboxAnswers = QtWidgets.QFormLayout()
        fboxAnswers.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        #fboxAnswers.setFormAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.scoreLabel = QtWidgets.QLabel()
        self.fcrLabel = QtWidgets.QLabel()
        self.interactLabel = QtWidgets.QLabel()
        self.communicationLabel = QtWidgets.QLabel()
        self.focusLabel = QtWidgets.QLabel()
        self.attitudeLabel = QtWidgets.QLabel()
        fboxAnswers.addRow("Overall:", self.scoreLabel)
        fboxAnswers.addRow("First contact resolution:", self.fcrLabel)
        fboxAnswers.addRow("Interaction Flow:", self.interactLabel)
        fboxAnswers.addRow("Communication:", self.communicationLabel)
        fboxAnswers.addRow("Customer Focus && Consultative Approach:", self.focusLabel)
        fboxAnswers.addRow("Appropriate Attitude && Demeanor:", self.attitudeLabel)

        self.tableView = QtWidgets.QTableView()
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        #spacer = QtWidgets.QSpacerItem(100,10)

        hbox_top_panel.addLayout(fboxFilters)
        hbox_top_panel.addLayout(fboxAnswers)
        hbox_top_panel.addStretch()
        #hbox_top_panel.addItem(spacer)
        hbox_top_panel.addLayout(vbox_button_panel)
        vbox_main_panel.addLayout(hbox_top_panel)
        vbox_main_panel.addWidget(self.tableView)
        vbox_main_panel.setStretchFactor(self.tableView,1)
        #vbox_button_panel.setAlignment(self.tableView,QtCore.Qt.AlignTop)
        widget.setLayout(vbox_main_panel)
        self.setCentralWidget(widget)
        self.setWindowTitle('Call Calibrations')
        self.setGeometry(160,160,900,600)

        self.yearFilter.addItems(('Any',))
        self.yearFilter.addItems(('2019','2018',))
        self.siteFilter.addItems(('Any',))
        self.siteFilter.addItems(('UK','SA','NK',))
        self.monthFilter.addItems(('Any',))
        self.monthFilter.addItems(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', ))
        self.monthFilter.addItems(('Aug', 'Sep', 'Oct', 'Nov', 'Dec',))
        self.weekFilter.setMaximum(52)
        self.weekFilter.setMinimum(0)
        self.weekFilter.setSpecialValueText("Any")
        self.agentFilter.addItem('Any')
        self.agentFilter.addItems(self.calibration.agent_values())
        #self.agentFilter.setMaxVisibleItems(10)
        #self.weekFilter.addItems(('Any',))
        #for counter in range(1,53):
            #self.weekFilter.addItem('Week ' + str(counter))
        #self.weekFilter.addItems(('01', '02','03', '04', '05', '06', '07'))
        
        self.calibrationModel = ScoreModel()
        # self.calibrationModel = QtGui.QStandardItemModel()
        self.update_table()
        
        addnew_button.clicked.connect(self.call_add_new_agent)
        save_button.clicked.connect(self.call_filter)
        cancel_button.clicked.connect(self.call_cancel)

        self.tableView.selectionModel().selectionChanged.connect(self.change_display_result)

    def change_display_result(self,selected,deselected):
        index_entity = self.tableView.selectionModel().selectedIndexes()
        self.store_loc = index_entity[0].row()
        #print('Row number: ' + str(index_entity[0].row()))
        self.store_site_value = self.calibrationModel.item(self.store_loc,3).text()
        #print('Current value: ' + self.store_site_value)
        #temp_entity = self.tableView.selectionModel().model()
        #for index in sorted(index_entity):
        #    print(str(temp_entity.data(index)))
    
    def scores_menu(self, QPos):
        self.scoresMenu = QtWidgets.QMenu()
        # menu_item = self.linksMenu.addAction("Remove Item")
        # menu_item = self.linksMenu.addAction(self.mark_viewed)
        self.scoresMenu.addAction(self.toggle_site)
        self.scoresMenu.addAction(self.toggle_site)
        parentPosition = self.tableView.mapToGlobal(QtCore.QPoint(0, 0))         
        self.scoresMenu.move(parentPosition + QPos)
        # self.linksMenu.move(QPos)
        self.scoresMenu.show()
    
    def createMenus(self):
        
        # Set up right-click menu for TableView
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.scores_menu)
        # Set up headline menus
        self.fileMenu = self.menuBar().addMenu("&File")
        self.editMenu = self.menuBar().addMenu("&Edit")
        # set up file menu
        self.fileMenu.addAction(self.export_calibrations)
        self.fileMenu.addAction(self.export_weekly_score)
    
    def update_table(self):

        input_list = self.calibration.calibration_filter(self.agentFilter.currentText(),
                                                        self.siteFilter.currentText(),
                                                        self.yearFilter.currentText(),
                                                        self.monthFilter.currentIndex(),
                                                        self.weekFilter.value())
        self.calibrationModel.clear()
        self.calibrationModel.setHorizontalHeaderLabels(('Week', 'Month', 'Agent', 'Site', 
                                                         'POS', 'Score', 'Interaction\nFlow',
                                                         'First\nContact\nResolution',
                                                         'Communication','Customer\nFocus',
                                                         'Demeanor', 'Feedback', 
                                                         'Manager\nReview', 
                                                         'Reviewed\nwith\nManager',
                                                         'Coaching\nDate', 'Review\nDate',
                                                         'Flight', 'Hotel', 'Rail', 'Car',))
        for row in input_list:
            row_list = []
            #row_list.append(QtGui.QStandardItem(row[0])) #date
            ccdate = datetime.strptime(row[0], "%Y-%m-%d")
            row_list.append(QtGui.QStandardItem(ccdate.strftime("%V"))) #week number
            row_list.append(QtGui.QStandardItem(ccdate.strftime("%b-%y"))) #Month-Year
            row_list.append(QtGui.QStandardItem(row[1])) #agent name
            row_list.append(QtGui.QStandardItem(row[2])) # site
            row_list.append(QtGui.QStandardItem(row[3])) # point of sale
            row_list.append(QtGui.QStandardItem(row[4])) # score
            row_list.append(QtGui.QStandardItem(row[5])) # InteractionFlow
            row_list.append(QtGui.QStandardItem(row[6])) # firstcontactresolution
            row_list.append(QtGui.QStandardItem(row[7])) # Communication
            row_list.append(QtGui.QStandardItem(row[8])) # CustomerFocus
            row_list.append(QtGui.QStandardItem(row[9])) # Demeanor
            row_list.append(QtGui.QStandardItem(row[10])) # Feedback
            row_list.append(QtGui.QStandardItem(row[11])) # ManagerReview
            row_list.append(QtGui.QStandardItem(row[12])) # ReviewedwithManager
            row_list.append(QtGui.QStandardItem(row[13])) # Coachingdate
            row_list.append(QtGui.QStandardItem(row[14])) # Reviewdate
            row_list.append(QtGui.QStandardItem(row[15])) # Flight
            row_list.append(QtGui.QStandardItem(row[16])) # Hotel
            row_list.append(QtGui.QStandardItem(row[17])) # Rail
            row_list.append(QtGui.QStandardItem(row[18])) # Car
            self.calibrationModel.appendRow(row_list)
        self.tableView.setModel(self.calibrationModel)
        self.tableView.resizeColumnsToContents()
        #self.tableView.resizeColumnToContents(0)
        #self.tableView.resizeColumnToContents(1)
        #self.tableView.resizeColumnToContents(2)
        #self.tableView.resizeColumnToContents(3)
        #self.tableView.resizeColumnToContents(4)
        self.tableView.setColumnWidth(11,300)
        self.tableView.setColumnWidth(13,70)
        self.tableView.setColumnWidth(14,70)
        self.tableView.setColumnWidth(15,50)

        try:
            self.calibration_summary['overall'] = mean([ int(row[4]) for row in input_list if row[4] != None ])
        except StatisticsError:
            self.calibration_summary['overall'] = 0
        try:
            self.calibration_summary['firstcontact'] = mean([ int(row[6]) for row in input_list if row[6] != None ])
        except StatisticsError:
            self.calibration_summary['firstcontact'] = 0
        try:
            self.calibration_summary['interactionflow'] = mean([ int(row[5]) for row in input_list if row[5] != None ])
        except StatisticsError:
            self.calibration_summary['interactionflow'] = 0
        try:
            self.calibration_summary['communication'] = mean([ int(row[7]) for row in input_list if row[7] != None ])
        except StatisticsError:
            self.calibration_summary['communication'] = 0
        try:
            self.calibration_summary['customerfocus'] = mean([ int(row[8]) for row in input_list if row[8] != None ])
        except StatisticsError:
            self.calibration_summary['customerfocus'] = 0
        try:
            self.calibration_summary['demeanor'] = mean([ int(row[9]) for row in input_list if row[9] != None ])
        except StatisticsError:
            self.calibration_summary['demeanor'] = 0
        
        self.scoreLabel.setText(f"{int(self.calibration_summary['overall']):02d}")
        self.fcrLabel.setText(f"{int(self.calibration_summary['firstcontact']):02d}")
        self.interactLabel.setText(f"{int(self.calibration_summary['interactionflow']):02d}")
        self.communicationLabel.setText(f"{int(self.calibration_summary['communication']):02d}")
        self.focusLabel.setText(f"{int(self.calibration_summary['customerfocus']):02d}")
        self.attitudeLabel.setText(f"{int(self.calibration_summary['demeanor']):02d}")
        
        #print('------')
        #print('Overall: ' + f"{int(self.calibration_summary['overall']):02d}")
        #print('First contact resolution: ' + f"{int(self.calibration_summary['firstcontact']):02d}")
        #print('Interaction Flow: ' + f"{int(self.calibration_summary['interactionflow']):02d}")
        #print('Communication: ' + f"{int(self.calibration_summary['communication']):02d}")
        #print('Customer Focus & Consultative Approach: ' + f"{int(self.calibration_summary['customerfocus']):02d}")
        #print('Appropriate Attitude & Demeanor: ' + f"{int(self.calibration_summary['demeanor']):02d}")
        #print('------')
        
    def call_filter(self):
        self.update_table()

    def call_cancel(self):
        self.close()

    def call_add_new_agent(self):

        self.hide()
        new_agent = {}
        success_value = False
        new_agent, success_value = CalibrationAddNew.getCalibrationDetails()
        self.show()
        print(new_agent)
        print(str(success_value))
        #try:
        #    current_agent = new_agent['agent']
        #except KeyError:
        #    return
        #if success_value and new_agent['agent']:
        if success_value:
            #if new_agent['agent'] == True:
            #if new_agent['new_agent'] == True:
                #Not necessary as insert is in the New form
                #self.calibration.insert_agent(new_agent['agent'])
            this_agent = self.calibration.get_agent_details(new_agent['agent'])
            print(this_agent)
            this_pos = self.calibration.get_pos_details(new_agent['pointofsale'])
            print(this_pos)
            self.calibration.insert_calibration(new_agent)
        self.update_table()

    def act_export_calibrations(self):
        pass

    def act_export_weekly_score(self):
        self.hide()
        #output_result = []
        #output_result = CalibrationExportSummary.getCalibrationDetails()
        _ = CalibrationExportSummary.getCalibrationDetails()
        self.show()

    def act_toggle_site(self):
        new_site = ""
        if self.store_site_value == "NK":
            new_site = "UK"
        elif self.store_site_value == "UK":
            new_site = "SA"
        elif self.store_site_value == "SA":
            new_site = "UK"
        else:
            new_site = "NK"
        self.calibrationModel.setItem(self.store_loc,3,QtGui.QStandardItem(new_site))

    def createActions(self):
        
        self.export_calibrations = QtWidgets.QAction("&Export calibrations", self, 
                  statusTip="Export calibrations as csv", triggered=self.act_export_calibrations)
        self.export_weekly_score = QtWidgets.QAction("Export &weekly score", self, 
                  statusTip="Export weekly score", triggered=self.act_export_weekly_score)
        self.toggle_site = QtWidgets.QAction("&Toggle site", self, 
                  statusTip="Toggle site", triggered=self.act_toggle_site)

class ScoreModel(QtGui.QStandardItemModel):

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            if index.column() in (0,1,3,5,6,7,8,9,10,12,13,14,15,16,17):
                #return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
                return QtCore.Qt.AlignCenter
            elif index.column() == 11:
                return QtCore.Qt.AlignTop
            #else:
                #return QtCore.Qt.AlignTop
        return super(ScoreModel, self).data(index, role)

def main():
    app = QtWidgets.QApplication([])

    win = CallCalibrationMain()
    win.show()
    win.raise_()
    app.exec_()

if __name__ == "__main__":
    main()