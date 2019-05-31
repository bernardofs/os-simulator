from process import *

class RP_FIFO():

	def add_pages_in_waiting_pages_from_processes(time: int):
		# adding all pages from processes in queue
		for process in self.processes:
			if process.arrival_time != time:
				continue
			for page in process.pages:
				self._waiting_pages.append(page)

	def __init__(self, processes: Process, elements_per_time: int):
		# queue to store the peges in the queue
		self._pages_in_RAM = []
		self._waiting_pages = []
		self.ram = RAM(50)
		self.disk = Disk()
		self.table = Table(50)
		self.blocked_processes = []
		self.waiting_processes = []
		self.processes = processes
		# elements por time defines how many elements will be added after one unit of time
		self._elements_per_time = elements_per_time

	def __get_first_pages_in_RAM(self):
		return self._pages_in_RAM[0]

	def __get_first_waiting_pages(self):
		return self._waiting_pages[0]

	def __get_and_delete_front_pages_in_RAM(self):
		front = self._pages_in_RAM[0]
		self._pages_in_RAM = self._pages_in_RAM[1:]
		return front

	def __get_and_delete_front_waiting_pages(self):
		front = self._waiting_pages[0]
		self._waiting_pages = self._waiting_pages[1:]
		return front

	def delete_first_elements_from_pages_in_RAM(self):
		cnt = self.elements_per_time
		while self._pages_in_RAM and cnt > 0:
			front = self.__get_and_delete_front_pages_in_RAM()
			self.ram.delete_page(front)
			self.disk.add_page(front)
			self._waiting_pages.append(front)
			cnt -= 1

	def add_first_waiting_pages(self):
		cnt = self.elements_per_time
		while self._waiting_pages and cnt > 0:
			front = self.__get_and_delete_front_waiting_pages()
			self.ram.add_page(front)
			self.disk.delete_page(front)
			self._pages_in_RAM.append(front)
			cnt -= 1

	def get_index_from_pid(self, pid: int):
		for i, process in enumerate(self.processes):
			if process.pid == pid:
				return i
		return -1

	# for each process it will be checked if its state is blocked or waiting
	def check_state(self):
		for process in self.processes:
			cnt_waiting = 0
			cnt_blocked = 0
			for page in process.pages:
				if page in self.ram.pages:
					cnt_waiting += 1
				elif page in self._waiting_pages
					cnt_blocked += 1

			# if page should be in waiting state
			if cnt_waiting == process._get_number_of_pages():
				if process not in self.waiting_processes:
					if process in self.blocked_processes:
						self.blocked_processes.remove(process)
					self.waiting_processes.append(process)
					# TODO CHANGE TABLE
			elif cnt_blocked > 0:
				if process not in self.blocked_processes
					if process in self.waiting_processes:
						self.waiting_processes.remove(process)
					self.blocked_processes.append(process)
			else 
				assert False


	def execute(time: int):

		self.add_pages_in_waiting_pages_from_processes(time)

		self.delete_first_elements_from_pages_in_RAM()

		self.add_first_waiting_pages()

