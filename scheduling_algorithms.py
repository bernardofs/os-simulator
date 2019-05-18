from process import *
from abc import ABC, abstractmethod

class Scheduling(ABC):  

    def __init__(self, processes: list):
        self.processes = processes   

    def add_process_at_the_end(self):
        pass    	

    def remove_process_at_the_beginning(self):
        pass

    def run_algorithm(self):
        pass

    def print_rect(self):
        pass

class FIFO(Scheduling):

    def __init__(self, processes: list):
        super().__init__(processes)

    def add_process_at_the_end(self, process: Process):
        self.processes.append(process)

    def get_first_process(self):
        return self.processes[0];

    def remove_process_at_the_beginning(self):
        self.processes = self.processes[1:]

    def print_rect(self, process: Process, t: int):
        print (process.number, ' ', t)

    def run_algorithm(self):

        t = 0
        while len(self.processes) > 0:
            front = self.get_first_process()
            self.remove_process_at_the_beginning()

            self.print_rect(front, t)
            t = t + 1

class FIFO(Scheduling):

    def __init__(self, processes: list):
        super().__init__(processes)

    def add_process_at_the_end(self, process: Process):
        self.processes.append(process)

    def get_first_process(self):
        return self.processes[0];

    def remove_process_at_the_beginning(self):
        self.processes = self.processes[1:]

    def print_rect(self, process: Process, t: int):
        print (process.number, ' ', t)

    def run_algorithm(self):

        t = 0
        while len(self.processes) > 0:
            front = self.get_first_process()
            self.remove_process_at_the_beginning()

            self.print_rect(front, t)
            t = t + 1

arr = [Process(1, 1, 2, 10,0,0,0), Process(9, 3, 2, 10,0,0,0), Process(3, 6, 1, 101,0,0,0)]

x = FIFO(arr)

x.run_algorithm()