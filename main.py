# -*- coding: utf-8 -*-
import sys


from PyQt4 import QtCore, QtGui
import random
import operator
from PyQt4.QtCore import QAbstractTableModel, SIGNAL
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
import xml.etree.cElementTree as ET

from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QStandardItem
from PyQt4.QtGui import QStandardItemModel
from PyQt4.QtGui import QTreeView

from participant_add import Participant_add_ui
from menu import MainMenu_ui
from team_add import Team_add_ui
from group_divide import Group_divide_ui
from participant_list import Participant_list_ui
from divided_view import Divided_view_ui

global header
header = ['Numer', 'Imie', 'Nazwisko', 'Druzyna']

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None):
        """
        Args:
            datain: a list of lists\n
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant().toPyObject()
        elif role != Qt.DisplayRole:
            return QVariant().toPyObject()
        return QVariant(self.arraydata[index.row()][index.column()]).toPyObject()

    def setData(self, index, value, role):
        pass         # not sure what to put here

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class Participant_add(QtGui.QWidget):
    global rowcount
    rowcount = 0
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui4 = Participant_add_ui()
        self.ui4.setupUi(self)
        global tv
        QtCore.QObject.connect(self.ui4.buttonBox, QtCore.SIGNAL("accepted()"), self.participant_add)
        participant_list_form = ex3
        tv = participant_list_form.ui3.tableView

    def participant_add(self):


        # set the table model
        #tablemdata = 0
        self.tablemodel = tv.model()
        #self.tablemodel.rowCount
        #tableclass = MyTableModel(tabledata, header, self)
        #rowcount = int(self.tablemodel.rowCount)


        # tabledata.remove([0])

        tablemodel = MyTableModel(tabledata, header, self)
        rowcount = tablemodel.rowCount(None)
        tabledata.append([rowcount + 1, str(self.ui4.lineEdit.text()), str(self.ui4.lineEdit_2.text()), 2])
        tv.setModel(tablemodel)
        self.save_participants_list()
        group_divide_form = ex2
        class_gr_divide = Group_divide()
        partic_number = str(class_gr_divide.get_participants_number)
        group_divide_form.ui.label_3.setText(
            "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">fd" + partic_number + "</span></p></body></html>")

    def save_participants_list(self):
        root = ET.Element("mainconfig")
        doc = ET.SubElement(root, "configdata")

        #model = MyTableModel(tabledata, header, self)
        model = ex3.ui3.tableView.model()
        # data = []
        rowcount = model.rowCount(None)
        for row in range(rowcount):
            # data.append([])

            index = model.index(row, 2)
            # We suppose data are strings
            # data[row].append(str(model.data(index).toString()))
            ET.SubElement(doc, "gpio_name_" + str(row), name="" + str(row) + str(model.data( index, Qt.DisplayRole)))

        tree = ET.ElementTree(root)
        tree.write("participants.xml")

class Team_add(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui6 = Team_add_ui()
        self.ui6.setupUi(self)

class Divided_view(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui8 = Divided_view_ui()
        self.ui8.setupUi(self)



class Participant_list(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui3 = Participant_list_ui()
        self.ui3.setupUi(self)


class Group_divide(QtGui.QWidget):
    global tabledata, participant_list_form, rowcount
    tabledata = []
    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        self.ui = Group_divide_ui()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.randomize_groups)
        #QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("textChanged(QString)"), self.update_divide_core)
        self.ui.lineEdit.textChanged.connect(self.update_divide_core)
        class_gr_divide = Group_divide
        partic_number = str(class_gr_divide.get_participants_number)
        self.ui.label_3.setText("<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">"+partic_number+"</span></p></body></html>")

    def update_divide_core(self):

        divided_to = int(self.ui.lineEdit.text())
        in_group = self.ui.lineEdit_2.text()

        in_group_ready = self.get_participants_number()/divided_to
        self.ui.lineEdit_2.setText(str(in_group_ready))
        #print in_group_ready

    def get_participants_number(self):
        participant_list_form = ex3
        # participant_list_form = Participant_list()
        # participant_list_form.show()
        tv = participant_list_form.ui3.tableView

        # set the table model
        tablemdata = 0



        # tabledata.remove([0])
        # tabledata.append([1, 1, 1, 1, 1])
        # table.model().layoutChanged.emit()
        tablemodel = MyTableModel(tabledata, header, tv)
        rowcount = int(tablemodel.rowCount(None))
        return int(rowcount)

    def randomize_groups(self):
        #participant_list_form = Participant_list()
        #participant_list_form.show()
        #participant_list_form.ui3.label.setText("sdsdfdsf")
        #ex2.ui.label_6.setText("test")
        participant_list_form = ex3
        # participant_list_form = Participant_list()
        # participant_list_form.show()
        tv = participant_list_form.ui3.tableView

        # set the table model
        tablemdata = 0
        #tabledata.append([2, 2, 2, 2, 2])
        # tabledata.remove([0])
        # tabledata.append([1, 1, 1, 1, 1])
        # table.model().layoutChanged.emit()
        tablemodel = MyTableModel(tabledata, header, self)
        rowcount = int(tablemodel.rowCount(None))
        tvmodel = tv.model()
        nums = [x+1 for x in range(rowcount)]
        random.shuffle(nums)

        print nums

        #iterating list





        #print i+1 % groups_to_create

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # init widgets
        view = ex8.ui8.treeView
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(header)
        view.setModel(model)
        view.setUniformRowHeights(True)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # populate data

        groups_to_create = int(self.ui.lineEdit.text())
        participants_in_group = int(self.ui.lineEdit_2.text())
        divider = 0
        group = 1
        parent1 = QStandardItem('Grupa {}'.format(group))
        for i, val in enumerate(nums):

            if divider == participants_in_group:
                divider = 0
                group = group + 1
                parent1 = QStandardItem('Grupa {}'.format(group))
            divider = divider + 1
            if val != 0:
                print "Grupa " + str(group) + " Osoby: " + str(val)
                self.tableindex_id = tablemodel.index (val-1,1)
                self.tableindex_surname = tablemodel.index (val-1,2)
                child1 = QStandardItem(str(val)+' '+" ")
                child2 = QStandardItem(str(tablemodel.data(self.tableindex_id,  Qt.DisplayRole)))
                child3 = QStandardItem(str(tablemodel.data(self.tableindex_surname,  Qt.DisplayRole)))
                parent1.appendRow([child1, child2, child3])


                model.appendRow(parent1)
                # span container columns
                view.setFirstColumnSpanned(i, view.rootIndex(), True)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # expand third container
        index = model.indexFromItem(parent1)
        view.expand(index)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # select last row
        selmod = view.selectionModel()
        index2 = model.indexFromItem(child3)
        selmod.select(index2, QItemSelectionModel.Select | QItemSelectionModel.Rows)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print i+1
        if i+1 > 3:
            print i / groups_to_create
        else:
            print i / groups_to_create

        #index = tablemodel.index(row, 1)

        print nums
        #print rowcount
        #print(random.randint(0, 9))
        #tv.setModel(tablemodel)
        #participant_list_form.tableView.c
        #participant_list_form.ui3.label.setText("dfgdg")


class MainMenu(QtGui.QWidget):
    #global self.participant_list_form
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui2 = MainMenu_ui()
        self.ui2.setupUi(self)


        #self.parentWidget().ui.
        QtCore.QObject.connect(self.ui2.pushButton_6 , QtCore.SIGNAL("clicked()"), self.open_participant_add_window)
        QtCore.QObject.connect(self.ui2.pushButton_5 , QtCore.SIGNAL("clicked()"), self.open_participant_list_window)
        QtCore.QObject.connect(self.ui2.pushButton_7 , QtCore.SIGNAL("clicked()"), self.open_group_divide_window)
        QtCore.QObject.connect(self.ui2.pushButton_4 , QtCore.SIGNAL("clicked()"), self.open_divided_view)
        QtCore.QObject.connect(self.ui2.pushButton_3 , QtCore.SIGNAL("clicked()"), self.save_data)
    def open_participant_add_window(self):
        self.participant_add_form = Participant_add()
        self.participant_add_form.show()

    def open_participant_list_window(self):
        participant_list_form = ex3
        #participant_list_form = Participant_list()
        participant_list_form.show()

    def open_group_divide_window(self):
        group_divide_form = ex2
        # participant_list_form = Participant_list()
        group_divide_form.show()

    def open_divided_view(self):
        divided_view_form = ex8
        # participant_list_form = Participant_list()
        divided_view_form.show()

    def save_data (self):
        root = ET.Element("mainconfig")
        doc = ET.SubElement(root, "configdata")

        model = ex3.ui3.tableView.model()
        # data = []

        for row in range(model.rowCount(None)):
            # data.append([])

            index = model.index(row, 1)

            # We suppose data are strings
            # data[row].append(str(model.data(index).toString()))
            ET.SubElement(doc, "participant_" + str(row), name="" + str(row)).text = str(model.data(index, Qt.DisplayRole))

        tree = ET.ElementTree(root)
        tree.write("participants.xml")







if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    #ex = MainMenu()
    #ex.show()
    global ex2, ex3, ex4, ex8
    ex2 = Group_divide()
    #ex2.show()
    ex3 = Participant_list()
    #ex3.show()
    ex4 = MainMenu()
    ex4.show()
    #ex5 = Participant_add()
    #ex5.show()
    ex8 = Divided_view()

    #myapp = Participant_add()
    #myapp.show()
sys.exit(app.exec_())
