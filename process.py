class Process:

    def __init__(self, number, arrival_time, exec_time, deadline):
        self.number = number
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.deadline = deadline

    def __init__(self, number, arrival_time, exec_time, deadline, priority, quantum, overhead):
        self.number = number
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.deadline = deadline
        self.priority = priority
        self.quantum = quantum
        self.overload = overhead