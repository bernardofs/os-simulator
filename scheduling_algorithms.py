from process import *
import operator
from abc import ABC, abstractmethod


class Scheduling(ABC):
    def __init__(self):
        self.turnaround = 0
        self.finished = True

    def add_process_at_the_end(self):
        self.cur_processes.append(process)

    def add_process_at_the_beginning(self, process: Process):
        self.cur_processes = [process] + self.cur_processes

    def remove_process_at_the_beginning(self):
        self.cur_processes = self.cur_processes[1:]

    def get_first_process(self):
        return self.cur_processes[0]

    def get_arrived_processes(self, t: int):
        while len(self.processes) > 0 and self.processes[0].arrival_time <= t:
            self.cur_processes.append(self.processes[0])
            self.processes = self.processes[1:]

    def set_executed(self, process: Process, ram: RAM):
        for page in process.pages:
            ram.set_executed(page)

    @abstractmethod
    def execute(self):
        pass


class Premptive(Scheduling):
    def __init__(self, quantum: int, overhead: int):
        self.quantum = quantum
        self.overhead = overhead
        self.cnt_quantum = 0
        self.cnt_overhead = -1
        super().__init__()


class Non_Premptive(Scheduling):
    def __init__(self):
        super().__init__()


class FIFO(Non_Premptive):
    def __init__(self):
        super().__init__()

    # returns the process executed and a flag determining whether it has finished
    def execute(self, waiting_processes: list, t: int, ram: RAM) -> (Process, bool):

        if len(waiting_processes) == 0:
            print("t = ", "empty")
            return Process(-1, -1, -1, -1, -1, -1), False

        front = waiting_processes[0]
        assert front.exec_time != 0
        print("front.exec_time", front.exec_time)
        self.set_executed(front, ram)

        if front.exec_time == 1:
            waiting_processes = waiting_processes[1:]
            self.turnaround = self.turnaround + (t - front.arrival_time + 1)
            self.finished = True
        else:
            waiting_processes[0].exec_time = waiting_processes[0].exec_time - 1
            self.finished = False
        return front, self.finished


class SJF(Non_Premptive):
    def __init__(self):
        super().__init__()

    def execute(self, waiting_processes: list, t: int, ram: RAM) -> (Process, bool):

        if len(waiting_processes) == 0:
            print("t = ", t, "empty")
            return Process(-1, -1, -1, -1, -1, -1), False

        if self.finished:
            waiting_processes.sort(key=lambda p: p.exec_time)
            self.finished = False

        front = waiting_processes[0]
        assert front.exec_time != 0
        print("front.exec_time", front.exec_time)
        self.set_executed(front, ram)

        finished = False
        if front.exec_time == 1:
            # waiting_processes = waiting_processes[1:]
            self.turnaround = self.turnaround + (t - front.arrival_time + 1)
            finished = True
        else:
            waiting_processes[0].exec_time = waiting_processes[0].exec_time - 1
            finished = False
        return front, finished


class Round_Robin(Premptive):
    def __init__(self, quantum: int, overhead: int):
        assert quantum >= 1 and overhead >= 1
        super().__init__(quantum=quantum, overhead=overhead)

    def execute(self, waiting_processes: list, t: int, ram: RAM) -> (Process, bool):

        # if cnt_overhead is negative, the process is executing
        if self.cnt_overhead >= 0:

            print("\n\n\n\nOVERHEAD\n\n\n\n")

            self.cnt_overhead += 1
            if self.cnt_overhead == self.overhead:
                self.cnt_overhead = -1
                self.cnt_quantum = 0
            return Process(-1, -1, -1, -1, -1, -1), False

        if len(waiting_processes) == 0:
            print("t = ", t, "empty")
            return Process(-1, -1, -1, -1, -1, -1), False

        front = waiting_processes[0]
        assert front.exec_time != 0
        print("front.exec_time", front.exec_time)
        self.set_executed(front, ram)

        finished = False
        if front.exec_time == 1:
            # waiting_processes = waiting_processes[1:]
            self.turnaround = self.turnaround + (t - front.arrival_time + 1)
            finished = True
            self.cnt_overhead = -1
            self.cnt_quantum = 0
        else:
            waiting_processes[0].exec_time = waiting_processes[0].exec_time - 1
            finished = False

        self.cnt_quantum += 1
        if self.cnt_quantum == self.quantum:
            self.cnt_overhead = 0
            self.cnt_quantum = 0
            # move process to the end of the queue if it will run again
            if not finished:
                waiting_processes = waiting_processes[1:] + [front]

        # returns a flag to indicates whether the process has finished and this process
        return front, finished


class EDF(Premptive):
    def __init__(self, quantum: int, overhead: int):
        self.quantum = quantum
        self.overhead = overhead
        super().__init__(quantum, overhead)

    def execute(self, waiting_processes: list, t: int, ram: RAM) -> (Process, bool):

        # if cnt_overhead is negative, the process is executing
        if self.cnt_overhead >= 0:
            print("\n\n\n\nOVERHEAD\n\n\n\n")
            self.cnt_overhead += 1
            if self.cnt_overhead == self.overhead:
                self.cnt_overhead = -1
                self.cnt_quantum = 0
            return Process(-1, -1, -1, -1, -1, -1), False

        if len(waiting_processes) == 0:
            print ("t = ", t, "empty")
            return Process(-1, -1, -1, -1, -1, -1), False

        if self.finished:
            waiting_processes.sort(key=lambda p: p.deadline)
            self.finished = False

        front = waiting_processes[0]
        assert front.exec_time != 0
        print("front.exec_time", front.exec_time)
        self.set_executed(front, ram)

        finished = False
        if front.exec_time == 1:
            # waiting_processes = waiting_processes[1:]
            self.turnaround = self.turnaround + (t - front.arrival_time + 1)
            finished = True
            self.cnt_overhead = -1
            self.cnt_quantum = 0
        else:
            waiting_processes[0].exec_time = waiting_processes[0].exec_time - 1
            finished = False

        self.cnt_quantum += 1
        if self.cnt_quantum == self.quantum:
            if not finished:
                self.cnt_overhead = 0
            self.cnt_quantum = 0
            # move process to the end of the queue if it will run again
            if not finished:
                waiting_processes = waiting_processes[1:] + [front]

        print('overhead =', self.cnt_overhead)
        # returns a flag to indicates whether the process has finished and this process
        return front, finished


# # Tests

# arr = [Process(1, 1, 2, 10, 0), Process(9, 3, 2, 10, 0), Process(3, 6, 1, 101, 0)]

# print('FIFO')
# x = FIFO(arr)
# x.execute()

# arr = [Process(1, 3, 3, 10, 0), Process(9, 4, 6, 10, 0), Process(3, 20, 3, 0, 0)]

# print('\nSJF')
# x = SJF(arr)
# x.execute()

# arr = [Process(1, 3, 3, 10, 0), Process(9, 4, 6, 10, 0), Process(3, 20, 3, 0, 0)]

# print('\nRR')
# x = Round_Robin(arr, 2, 1)
# x.execute()

# arr = [Process(1, 3, 3, 12, 5), Process(9, 4, 6, 11, 10), Process(3, 20, 3, 0, 3)]

# print('\nEDF')
# x = EDF(arr, 2, 1)
# x.execute()
