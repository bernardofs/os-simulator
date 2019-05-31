class Page:

	def __init__(self, associated_pid_process: int, process_index: int, index_in_RAM: int):
		self.associated_pid_process = associated_pid_process
		self.process_index = process_index

class Table:

	# - if pid is equal to -1 in an index of the table, then this index is empty 
	# - table initializes empty
	def __init__(self, table_size: int):
		self.pages = [Page(-1, -1)]*table_size
		# if its -1, there's no element, if it's 0 it's on disk, if it's 1 it's on RAM
		self.present = [-1]*table_size
		self.ptr = 0

	def add_page(self, page: Page):
		self.pages[self.ptr] = page
		self.present[i] = 1
		self.ptr = (self.ptr + 1) % len(self.pages)
		

	def delete_page(self, page: Page):
		for i, page_in_list in enumerate(self.pages):
			if page_in_list == page:
				self.pages[i] = Page(-1, -1)
				self.present[i] = -1
				return

class Process:

    def __init__(self, pid: int, arrival_time: int, exec_time: int, deadline: int, priority: int, number_of_pages: int):
        self.__pid = pid
        self.__arrival_time = arrival_time
        self.__exec_time = exec_time
        self.__deadline = deadline
        self.__priority = priority
        self.__pages = [Page(pid, i) for i in range(number_of_pages)]
        self.__pages_in_RAM = 0

    # checks whether the process is ready to execute
    # returns false if it is blocked
    def is_ready(self) -> bool:
    	return self.pages_in_RAM == len(self.pages)

    def get_number_of_pages(self):
    	return len(pages)

class Disk:

	def __init__(self):
		self.pages = []

	def add_page(self, page: Page):
		self.pages.append(page)

	def delete_page(self, page: Page):
		for i, page_in_list in enumerate(self.pages):
			if page == page_in_list:
				del self.pages[i]
				return

class RAM:

	# - if pid is equal to -1 in an index of the RAM, then this index is empty 
	# - RAM initializes empty
	def __init__(self, RAM_size: int):
		self.pages = [Page(-1, -1)]*RAM_size
		self.executed = [False]*RAM_size
		self.RAM_size = RAM_size

	def get_index(self, page: Page):
		for i, page_in_list in enumerate(self.pages):
			if page == page_in_list:
				return i

	def __get_first_empty_page(self):
		for i, page in enumerate(self.pages):
			if page.associated_pid_process = -1:
				return i
		return -1

	def add_page(self, page: Page):
		RAM_idx = get_first_empty_page()
		self.pages[RAM_idx] = page
		self.executed[i] = False

	def delete_page(self, page: Page):
		idx = get_index(page)
		self.pages[idx] = Page(-1, -1)
		for i, page_in_list in enumerate(self.pages):
			if page == page_in_list:
				self.pages[i] = Page(-1, -1)
				return
