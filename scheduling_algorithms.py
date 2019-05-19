from process import *
import operator
from abc import ABC, abstractmethod

class Scheduling(ABC):

    def __init__(self, processes: list):
        self.processes = processes
        self.cur_processes = []

    def add_process_at_the_end(self):
        self.cur_processes.append(process)

    def add_process_at_the_beginning(self, process: Process):
        self.cur_processes = [process] + self.cur_processes        

    def remove_process_at_the_beginning(self):
        self.cur_processes = self.cur_processes[1:]

    def get_first_process(self):
        return self.cur_processes[0];

    def get_arrived_processes(self, t: int):
        while (len(self.processes) > 0 and self.processes[0].arrival_time <= t):
            self.cur_processes.append(self.processes[0])
            self.processes = self.processes[1:]

    @abstractmethod
    def run_algorithm(self):
        pass

    def print_rect(self):
        pass

class FIFO(Scheduling):

    def __init__(self, processes: list):
        super().__init__(processes)

    def print_rect(self, process: Process, t: int):
        print (process.number, ' ', t)


    def run_algorithm(self):

        self.processes.sort(key=lambda p: p.arrival_time)
        t = 0
        while len(self.processes) > 0 or len(self.cur_processes) > 0:

            self.get_arrived_processes(t)

            if(len(self.cur_processes) == 0):
                print ('t = ', t, 'empty')
                t = t + 1
                continue

            front = self.get_first_process()
            self.remove_process_at_the_beginning()

            self.print_rect(front, t)
            t = t + 1
            self.get_arrived_processes(t)
            front.exec_time = front.exec_time - 1
            if front.exec_time > 0:
                self.add_process_at_the_beginning(front)

class SJF(Scheduling):

        def __init__(self, processes: list):
            super().__init__(processes)

        def print_rect(self, process: Process, t: int):
            print (process.number, process.exec_time, t)

        def run_algorithm(self):

            self.processes.sort(key=lambda p: p.arrival_time)

            t = 0
            while len(self.processes) > 0 or len(self.cur_processes) > 0:

                self.get_arrived_processes(t)

                if(len(self.cur_processes) == 0):
                    print ('t = ', t, 'empty')
                    t = t + 1
                    continue

                self.cur_processes.sort(key=lambda p: p.exec_time)
                front = self.get_first_process()
                self.remove_process_at_the_beginning()

                self.print_rect(front, t)
                front.exec_time = front.exec_time - 1
                t = t + 1

                if front.exec_time > 0:
                    self.add_process_at_the_beginning(front)


class Round_Robin(Scheduling):

    def __init__(self, processes: list, quantum: int, overhead: int):
        self.quantum = quantum
        self.overhead = overhead
        super().__init__(processes)

    def print_rect(self, process: Process, t: int):
        print (process.number, process.exec_time, t)

    def apply_overhead(self):
        cnt = self.overhead
        while(cnt > 0):
            print ("overhead")
            cnt = cnt - 1

    def run_algorithm(self):
        
        self.processes.sort(key=lambda p: p.arrival_time)
        # for x in self.processes:
        #     print (x.arrival_time)

        t = 0
        while len(self.processes) > 0 or len(self.cur_processes) > 0:

            self.get_arrived_processes(t)

            if(len(self.cur_processes) == 0):
                print ('t = ', t, 'empty')
                t = t + 1
                continue

            front = self.get_first_process()
            self.remove_process_at_the_beginning()

            time_of_execution = min(self.quantum, front.exec_time)
            while (time_of_execution > 0):
                self.print_rect(front, t)
                time_of_execution = time_of_execution - 1
                t = t + 1

            self.get_arrived_processes(t)

            if front.exec_time > self.quantum:
                front.exec_time -= self.quantum
                self.cur_processes.append(front)
                self.apply_overhead()
                t = t + self.overhead


class EDF(Scheduling):

    def __init__(self, processes: list, quantum: int, overhead: int):
        self.quantum = quantum
        self.overhead = overhead
        super().__init__(processes)

    def print_rect(self, process: Process, t: int):
        print (process.number, process.exec_time, t)

    def apply_overhead(self):
        cnt = self.overhead
        while(cnt > 0):
            print ("overhead")
            cnt = cnt - 1

    def run_algorithm(self):

        self.processes.sort(key=lambda p: p.arrival_time)

        t = 0
        while len(self.processes) > 0 or len(self.cur_processes) > 0:

            self.get_arrived_processes(t)

            if(len(self.cur_processes) == 0):
                print ('t = ', t, 'empty')
                t = t + 1
                continue            

            self.cur_processes.sort(key=lambda p: p.deadline)
                
            front = self.get_first_process()
            self.remove_process_at_the_beginning()

            time_of_execution = min(self.quantum, front.exec_time)
            while (time_of_execution > 0):
                self.print_rect(front, t)
                time_of_execution = time_of_execution - 1
                t = t + 1

            self.get_arrived_processes(t)

            if front.exec_time > self.quantum:
                front.exec_time -= self.quantum
                self.cur_processes.append(front)
                self.apply_overhead()
                t = t + self.overhead

# Tests

arr = [Process(1, 1, 2, 10, 0), Process(9, 3, 2, 10, 0), Process(3, 6, 1, 101, 0)]

print('FIFO')
x = FIFO(arr)
x.run_algorithm()

arr = [Process(1, 3, 3, 10, 0), Process(9, 4, 6, 10, 0), Process(3, 20, 3, 0, 0)]

print('\nSJF')
x = SJF(arr)
x.run_algorithm()

arr = [Process(1, 3, 3, 10, 0), Process(9, 4, 6, 10, 0), Process(3, 20, 3, 0, 0)]

print('\nRR')
x = Round_Robin(arr, 2, 1)
x.run_algorithm()

arr = [Process(1, 3, 3, 12, 5), Process(9, 4, 6, 11, 10), Process(3, 20, 3, 0, 3)]

print('\nEDF')
x = EDF(arr, 2, 1)
x.run_algorithm()
