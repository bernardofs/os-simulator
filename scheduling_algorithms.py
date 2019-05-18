from process import *
import operator
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

    def apply_overhead(self):
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

class Round_Robin(Scheduling):

    def __init__(self, processes: list, quantum: int, overhead: int):
        self.quantum = quantum
        self.overhead = overhead
        super().__init__(processes)

    def add_process_at_the_end(self, process: Process):
        self.processes.append(process)

    def get_first_process(self):
        return self.processes[0];

    def remove_process_at_the_beginning(self):
        self.processes = self.processes[1:]

    def print_rect(self, process: Process, t: int):
        print (process.number, process.exec_time, t)

    def apply_overhead(self):
        copy = self.overhead
        while(copy > 0):
            print ("overhead")
            copy = copy - 1

    def run_algorithm(self):

        self.processes = sorted(self.processes)
        for x in self.processes:
            print (x.arrival_time)
        cur_processes = []

        t = 0
        while len(self.processes) > 0 or len(cur_processes) > 0:

            while (len(self.processes) > 0 and self.get_first_process().arrival_time <= t):
                cur_processes.append(self.get_first_process())
                self.remove_process_at_the_beginning()

            if(len(cur_processes) == 0):
                print ('t = ', t, 'empty')
                t = t + 1
                continue

            front = cur_processes[0]
            cur_processes = cur_processes[1:]

            time_of_execution = min(self.quantum, front.exec_time)
            while (time_of_execution > 0):
                self.print_rect(front, t)
                time_of_execution = time_of_execution - 1
                t = t + 1

            while (len(self.processes) > 0 and self.get_first_process().arrival_time <= t):
                cur_processes.append(self.get_first_process())
                self.remove_process_at_the_beginning()

            if front.exec_time > self.quantum:
                front.exec_time -= self.quantum
                cur_processes.append(front)
                self.apply_overhead()
                t = t + self.overhead 


# Tests

arr = [Process(1, 1, 2, 10, 0), Process(9, 3, 2, 10, 0), Process(3, 6, 1, 101, 0)]

print('FIFO')
x = FIFO(arr)
x.run_algorithm()

arr = [Process(1, 3, 3, 10, 0), Process(9, 4, 6, 10, 0), Process(3, 20, 3, 0, 0)]

print('\nRR')
x = Round_Robin(arr, 2, 1)
x.run_algorithm()