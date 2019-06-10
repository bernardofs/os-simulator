from scheduling_algorithms import *
from replacing_pages_algorithms import *
from components import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
from PyQt5 import QtTest



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Trabalho SO'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 300
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

    def addPageRam(self, tabela):
        self.tableWidget.setColumnCount(50)
        self.tableWidget.setRowCount(1)
        # for page in pages:
        #     self.tableWidget.setItem(0, page.process_index, QTableWidgetItem( "Processo " + str(page.associated_pid_process) ))
        for i, page in enumerate(tabela):
            if  page.associated_pid_process == -1: 
                self.tableWidget.setItem(0, i, QTableWidgetItem( "Lixo"))
                self.tableWidget.item(0,i).setBackground(QtGui.QColor(255,0,0)) 
            else:
                self.tableWidget.setItem(0, i, QTableWidgetItem( "Processo " + str(page.associated_pid_process) ))
                self.tableWidget.item(0, i).setBackground(QtGui.QColor(0,128,0))
                
         

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
    	if ans == QMessageBox.Ok:
            self.close()
            sys.exit()
        # msg = QMessageBox()
    	# msg.setIcon(QMessageBox.Information)
    	# msg.setWindowTitle("Turnaround")
    	# msg.setText(str(turnaround))
    	# msg.setStandardButtons(QMessageBox.Ok)
    	# msg.show()
    def escolhaPro(self):
        algo = ("FIFO","SJF","Round_Robin","EDF")
        algo, okPressed = QInputDialog.getItem(self,"","Algoritmos Escalonamento: ", algo, 0, False)
        if okPressed and algo:
            print(algo)
            return algo

    def escolhaPag(self):
        pag = ("FIFO","LRU")
        pag, okPressed = QInputDialog.getItem(self,"","Algoritmos Troca de paginas: ", pag, 0, False)
        if okPressed and pag:
            print(pag)
            return pag   

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

#arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 1, 2, 0, 0, 5), Process(3, 2, 3, 0, 0, 2)]
#arr = [Process(1, 0, 4, 0, 0, 5), Process(2, 0, 2, 3, 0, 1), Process(3, 0, 1, 2, 0, 1), Process(4, 0, 4, 1, 0, 3)]
#arr = [Process(1, 0, 3, 0, 0, 5), Process(2, 0, 3, 0, 0, 5)]
#arr = [Process(1, 0, 2, 4, 0, 1), Process(2, 0, 1, 0, 0, 1), Process(3, 0, 2, 2, 0, 4)]
#arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 1, 3, 0, 0, 4), Process(3,2 , 4, 0, 0, 3)]

def main():

    app = QApplication(sys.argv)
    ex = App()
    ram = App()
    #disco = App()

    processo = ex.escolhaPro()
    pagina = ex.escolhaPag()
    print(processo)
    print(pagina)
    QtTest.QTest.qWait(1000)
    replacing_pages_algorithm = pagina
    scheduling_algorithm = processo
    print(scheduling_algorithm)
    print(replacing_pages_algorithm)

    print("start")
    # rp = RP_FIFO(arr, 2)
    # rp = RP_LRU(arr, 2)
    # f = FIFO()
    # f = SJF()
    # f = Round_Robin(2, 1)
    # f = EDF(2, 1)

    if replacing_pages_algorithm == "FIFO":
        print("-------------------------------------ue")
        rp = RP_FIFO(arr, 2)
    if replacing_pages_algorithm == "LRU":
        rp = RP_LRU(arr, 2)

    if scheduling_algorithm == "FIFO":
        f = FIFO()
    elif scheduling_algorithm == "SJF":
        f = SJF()
    elif scheduling_algorithm == "Round_Robin":
        print("foi")
        f = Round_Robin(quantum, sobrecarga)
    elif scheduling_algorithm == "EDF":
        f = EDF(quantum, sobrecarga)

    t = 0
    lastpid=1
    #disco.criarDisco(disco, arr)
    while rp.there_is_processes():
        
        print("\n\n\n\n\n\n\n")

        rp.execute()

        process, finished = f.execute(rp.waiting_processes, t, rp.ram)
        
        if finished:
            rp.running_process_pid = -1
            print ('finished')
            rp.delete_process(process)
        else:
            if replacing_pages_algorithm == "LRU":
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
        ram.addPageRam( rp.table.pages )
        if rp.running_process_pid > -1:
            lastpid = rp.running_process_pid
            ex.addColumn(t)
            ex.addProcessTable(rp.running_process_pid,t)
            QtTest.QTest.qWait(time)
        else:
        	ex.addColumn(t)
        	ex.addSobrecarga(lastpid, t)
        	QtTest.QTest.qWait(time)


    print ('TURNAROUND = ', f.turnaround / len(arr))
    aux = f.turnaround / len(arr)
    ex.fimEscalonador(aux)
    sys.exit(app.exec_())

if __name__ == "__main__":
    while 1:
        print("Quantos processos? ")
        qtProcessos = int(input())
        pid = 1
        arr = []
        print("Quantum: ")
        quantum = int(input())
        print("Sobrecarga: ")
        sobrecarga = int(input())
        print("Velocidade do Grafico: ")
        time = int(input())
        disco = 0
        while qtProcessos > 0:
            print("-----Processo ",pid,"-----")
            print("Tempo de chegada: ")
            arrival = int(input())
            print("Tempo de execução: ")
            execTime = int(input())
            print("Deadline: ")
            deadline = int(input())
            print("Prioridade: ")
            priority = int(input())
            print("Numero de Páginas: ")
            pages = int(input())
            disco+=pages
            arr.append(Process(pid, arrival, execTime, deadline, priority, pages))
            pid += 1
            qtProcessos -= 1
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
