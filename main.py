from scheduling_algorithms import *
from replacing_pages_algorithms import *
from components import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
from PyQt5 import QtTest

BLUE = QtGui.QColor(100,100,150)

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Trabalho SO'
        self.left = 0
        self.top = 0
        self.width = 900
        self.height = 600
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()     
    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(arr))
        self.tableWidget.setColumnCount(1)        
        self.tableWidget.move(0,0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
    def addColumn(self, newTam):
        print("Flag");
        self.tableWidget.setColumnCount(newTam)

    def addProcessTable(self, pid, time):
        print("pid: ",pid," time: ", time)
        pid = pid-1
        self.tableWidget.setItem(pid, time-1, QTableWidgetItem("Executando"))
        self.tableWidget.item(pid, time-1).setBackground(QtGui.QColor(0,128,0))
    
    def addSobrecarga(self, lastpid, time):
    	lastpid = lastpid-1
    	self.tableWidget.setItem(lastpid,time-1,QTableWidgetItem("Sobrecarga"))
    	self.tableWidget.item(lastpid,time-1).setBackground(QtGui.QColor(255,0,0))    
    
    def fimEscalonador(self, turnaround):
    	ans = QMessageBox.information(self, "Turnaround", "Turnaround = "+str(turnaround), QMessageBox.Ok, QMessageBox.Cancel)
    	# msg = QMessageBox()
    	# msg.setIcon(QMessageBox.Information)
    	# msg.setWindowTitle("Turnaround")
    	# msg.setText(str(turnaround))
    	# msg.setStandardButtons(QMessageBox.Ok)
    	# msg.show()

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

#arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 1, 2, 0, 0, 5), Process(3, 2, 3, 0, 0, 2)]
#arr = [Process(1, 0, 4, 0, 0, 5), Process(2, 0, 2, 3, 0, 1), Process(3, 0, 1, 2, 0, 1), Process(4, 0, 4, 1, 0, 3)]
#arr = [Process(1, 0, 3, 0, 0, 5), Process(2, 0, 3, 0, 0, 5)]
#arr = [Process(1, 0, 2, 4, 0, 1), Process(2, 0, 1, 0, 0, 1), Process(3, 0, 2, 2, 0, 4)]
arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 1, 3, 0, 0, 4), Process(3,2 , 4, 0, 0, 3)]

def main():

    app = QApplication(sys.argv)
    ex = App()

    replacing_pages_algorithm = 'FIFO'
    scheduling_algorithm = 'FIFO'

    print("start")
    # rp = RP_FIFO(arr, 2)
    # rp = RP_LRU(arr, 2)
    # f = FIFO()
    # f = SJF()
    # f = Round_Robin(2, 1)
    # f = EDF(2, 1)

    if replacing_pages_algorithm == 'FIFO':
        rp = RP_FIFO(arr, 2)
    if replacing_pages_algorithm == 'LRU':
        rp = RP_LRU(arr, 2)

    if scheduling_algorithm == 'FIFO':
        f = FIFO()
    elif scheduling_algorithm == 'SJF':
        f = SJF()
    elif scheduling_algorithm == 'Round_Robin':
        f = Round_Robin(2, 1)
    elif scheduling_algorithm == 'EDF':
        f = EDF(2, 1)

    t = 0
    lastpid=1
    while rp.there_is_processes():
        
        print("\n\n\n\n\n\n\n")

        rp.execute()

        process, finished = f.execute(rp.waiting_processes, t, rp.ram)
        if finished:
            rp.running_process_pid = -1
            print ('finished')
            rp.delete_process(process)
        else:
            if replacing_pages_algorithm == 'LRU':
                rp.update_pages_frequency_of_a_process(process) 

        t += 1

        rp.running_process_pid = process.pid
        print("rp.running_process_pid", rp.running_process_pid)
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        if rp.running_process_pid > -1:
            lastpid = rp.running_process_pid
            ex.addColumn(t)
            ex.addProcessTable(rp.running_process_pid,t)
            QtTest.QTest.qWait(100)
        else:
        	ex.addColumn(t)
        	ex.addSobrecarga(lastpid, t)
        	QtTest.QTest.qWait(100)


    print ('TURNAROUND = ', f.turnaround / len(arr))
    aux = f.turnaround / len(arr)
    ex.fimEscalonador(aux)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    # app = QApplication(sys.argv)
    # ex = App()
    # tam = int(input())
    # print("o tam foi ",tam)
    # ex.addTable(tam)

    # tam = int(input())
    # print("o tam foi ",tam)
    # ex.addTable(tam)
    # sys.exit(app.exec_())
