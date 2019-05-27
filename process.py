class Page:

	def __init__(self, associated_pid_process: int, process_index: int, index_in_RAM: int):
		self.associated_pid_process = associated_pid_process
		self.process_index = process_index
		# if index_in_RAM is equal to -1 it is not present in RAM
		self.index_in_RAM = index_in_RAM

class Table:

	# - if pid is equal to -1 in an index of the table, then this index is empty 
	# - table initializes empty
	def __init__(self, table_size: int):
		self.pages = [Page(-1, -1, False)]*table_size

class Process:

    def __init__(self, pid: int, arrival_time: int, exec_time: int, deadline: int, priority: int, number_of_pages: int):
        self.__pid = pid
        self.__arrival_time = arrival_time
        self.__exec_time = exec_time
        self.__deadline = deadline
        self.__priority = priority
        self.__pages = [Page(pid, i, False) for i in range(number_of_pages)]
        self.__pages_in_RAM = 0

    # checks whether the process is ready to execute
    # returns false if it is blocked
    def is_ready(self) -> bool:
    	return self.pages_in_RAM == len(self.pages)

    def get_number_of_pages(self):
    	return len(pages)

class RAM:

	# - if pid is equal to -1 in an index of the RAM, then this index is empty 
	# - RAM initializes empty
	def __init__(self, RAM_size: int):
		self.pages = [Page(-1, -1, False)]*RAM_size

	
