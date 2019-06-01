from process import *

class RP_FIFO():

	def __init__(self, processes: Process, elements_per_time: int):
		# queue to store the pages in the RAM
		self._pages_in_RAM = []
		# queue to store pages which are waiting to enter in RAM
		self._waiting_pages = []
		self.ram = RAM(5)
		self.disk = Disk()
		self.table = Table(5)
		self.time = 0
		self.blocked_processes = []
		self.waiting_processes = []
		self.processes = processes
		self.cur_processes = processes.copy()
		self.back_processes = processes.copy()
		# elements por time defines how many elements will be added after one unit of time
		self.elements_per_time = elements_per_time
		self.running_process_pid = -1

	def add_pages_in_waiting_pages_from_processes(self):
		# adding all pages from processes in queue
		for process in self.back_processes:
			if process.arrival_time != self.time:
				continue
			self.cur_processes.remove(process)
			for page in process.pages:
				self._waiting_pages.append(page)

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

	def delete_a_page_in_RAM(self):
		# this element must be executed at least once and 
		# it shouldn't be running at the moment
		for page in self._pages_in_RAM:
			if self.ram.was_executed(page) and self.running_process_pid != page.associated_pid_process:
				deleted = page
				self._pages_in_RAM.remove(deleted)
				self.ram.delete_page(front)
				return deleted

		return Page(-1, -1)

	def delete_first_elements_from_pages_in_RAM(self):
		cnt = max(0, self.elements_per_time - (self.ram.RAM_size - len(self._pages_in_RAM)))
		while self._pages_in_RAM and cnt > 0:
			front = self.delete_a_page_in_RAM()
			if front.associated_pid_process == -1:
				return
			self.disk.add_page(front)
			self._waiting_pages.append(front)
			cnt -= 1

	def add_first_waiting_pages(self):
		cnt = self.elements_per_time
		while self._waiting_pages and cnt > 0:
			front = self.__get_and_delete_front_waiting_pages()
			added = self.ram.add_page(front)
			# if theres not a valid page to add
			if added == -1:
				self._waiting_pages = [front] + self._waiting_pages
				return
			self.disk.delete_page(front)
			self._pages_in_RAM.append(front)
			cnt -= 1

	def get_index_from_pid(self, pid: int):
		for i, process in enumerate(self.processes):
			if process.pid == pid:
				return i
		return -1

	def delete_process(self, process: Process):
		if process in self.waiting_processes:
			self.waiting_processes.remove(process)
		if process in self.blocked_processes:
			self.blocked_processes.remove(process)
		for i in range(process.get_number_of_pages()):
			self._pages_in_RAM.remove(Page(process.pid, i))
			self.ram.delete_page(Page(process.pid, i))

	# for each process it will be checked if its state is blocked or waiting
	def check_state(self):
		print(len(self.processes))
		for process in self.processes:
			cnt_waiting = 0
			cnt_blocked = 0
			for page in process.pages:
				if page in self.ram.pages:
					cnt_waiting += 1
				elif page in self._waiting_pages:
					cnt_blocked += 1

			# if page should be in waiting state
			if cnt_waiting == process.get_number_of_pages():
				if process not in self.waiting_processes:
					if process in self.blocked_processes:
						self.blocked_processes.remove(process)
					self.waiting_processes.append(process)
					# TODO CHANGE TABLE
			elif cnt_blocked > 0:
				if process not in self.blocked_processes:
					if process in self.waiting_processes:
						self.waiting_processes.remove(process)
					self.blocked_processes.append(process)

	def there_is_processes(self) -> bool:
		return len(self.cur_processes) == 0

	def execute(self):

		self.add_pages_in_waiting_pages_from_processes()

		self.delete_first_elements_from_pages_in_RAM()

		self.add_first_waiting_pages()

		self.ram.print()

		self.check_state()
		print ('pages in ram')
		for page in self._pages_in_RAM:
			print (page.associated_pid_process, page.process_index)
		print ('_waiting_pages')
		for page in self._waiting_pages:
			print (page.associated_pid_process, page.process_index)
		print ('blocked_processes')
		for process in self.blocked_processes:
			print (process.pid)
		print ('waiting_processes')
		for process in self.waiting_processes:
			print (process.pid)

		self.time += 1

