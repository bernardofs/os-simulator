class RP_FIFO():

	def add_pages_in_queue_from_processes(processes: Process):
		# adding all pages from processes in queue
		for process in processes:
			for page in process.pages:
				self.queue.put(page)

	def __init__(self, processes: Process, elements_per_time: int):
		self.__queue = queue.Queue()
		add_pages_in_queue_from_processes(processes)
		self.__elements_per_time = elements_per_time

	def get_first_elements_from_queue() -> list:
		cnt = self.elements_per_time
		ans = []
		while __queue.empty() == False and cnt > 0:
			ans.append(__queue.get())
			cnt -= 1
		return ans

	def add_elements_in_queue(pages: Page):
		for p in pages:
			__queue.put(p)




