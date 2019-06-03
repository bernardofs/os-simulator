from components import *

class Replacing_Pages:
    def __init__(self, processes: Process, elements_per_time: int):
        # queue to store the pages in the RAM
        self._pages_in_RAM = []
        # queue to store the pages in the disk
        self._pages_in_disk = []
        # queue to store pages which are waiting to enter in RAM that are neither
        # in RAM or in disk
        self._waiting_pages = []
        self.ram = RAM(5)
        self.disk = Disk()
        self.table = Table(15)
        self.time = 0
        self.blocked_processes = processes.copy()
        self.waiting_processes = []
        self.processes = processes
        self.cur_processes = processes.copy()
        self.back_processes = processes.copy()
        # elements por time defines how many elements will be added after one unit of time
        self.elements_per_time = elements_per_time
        self.running_process_pid = -1

    def get_index_from_pid(self, pid: int):
        for i, process in enumerate(self.processes):
            if process.pid == pid:
                return i
        return None

    def delete_process(self, process: Process):
        if process in self.waiting_processes:
            self.waiting_processes.remove(process)
        if process in self.blocked_processes:
            self.blocked_processes.remove(process)
        for i in range(process.get_number_of_pages()):
            page = Page(process.pid, i)
            # if page in self._pages_in_RAM:
            self._pages_in_RAM.remove(page)
            self.ram.delete_page(page)
            self.disk.delete_page(page)
            self.table.delete_page(page)

    # for each process it will be checked if its state is blocked or waiting
    def check_state(self):

        for process in self.processes:
            cnt_waiting = 0
            cnt_blocked = 0
            for page in process.pages:
                if page in self.ram.pages:
                    cnt_waiting += 1
                elif page in self._waiting_pages or page in self._pages_in_disk:
                    cnt_blocked += 1

            # if page should be in waiting state
            if cnt_waiting == process.get_number_of_pages():
                if process not in self.waiting_processes:
                    self.waiting_processes.append(process)
                    if process in self.blocked_processes:
                        self.blocked_processes.remove(process)
            else:
                if process not in self.blocked_processes:
                    self.blocked_processes.append(process)
                    if process in self.waiting_processes:
                        self.waiting_processes.remove(process)

    def there_is_processes(self) -> bool:
        return (
            len(self.cur_processes)
            + len(self._waiting_pages)
            + len(self._pages_in_RAM)
            + len(self._pages_in_disk)
            > 0
        )
    

    def sort_waiting_processes_by_exec_time(self):
        self.waiting_processes.sort(key=lambda p: p.exec_time)

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

    def __get_and_delete_front_pages_in_disk(self):
        front = self._pages_in_disk[0]
        self._pages_in_disk = self._pages_in_disk[1:]
        return front

    def __get_and_delete_front_waiting_pages(self):
        front = self._waiting_pages[0]
        self._waiting_pages = self._waiting_pages[1:]
        return front

    def __get_number_of_pages_to_be_added(self):
        return min(
            len(self._pages_in_disk) + len(self._waiting_pages), self.elements_per_time
        )

    def delete_a_page_in_RAM(self):
        # this element must be executed at least once and
        # it shouldn't be running at the moment
        for page in self._pages_in_RAM:
            if (
                self.ram.was_executed(page)
                and self.running_process_pid != page.associated_pid_process
            ):
                deleted = page
                self._pages_in_RAM.remove(deleted)
                self.ram.delete_page(deleted)
                self.disk.add_page(deleted)
                self.table.set_not_present_in_RAM(deleted)
                self._pages_in_disk.append(deleted)
                return deleted

        return Page(-1, -1)

    def delete_first_elements_from_pages_in_RAM(self):
        # cnt represents the number of pages to be removed
        cnt = self.__get_number_of_pages_to_be_added()
        while self._pages_in_RAM and cnt > 0:
            front = self.delete_a_page_in_RAM()
            if front.associated_pid_process == -1:
                return
            cnt -= 1

    def add_first_pages_to_RAM(self):

        cnt = self.elements_per_time

        # adding all pages from disk to ram
        while (
            self._pages_in_disk
            and len(self._pages_in_RAM) < self.ram.RAM_size
            and cnt > 0
        ):
            front = self.__get_and_delete_front_pages_in_disk()
            idx_in_RAM = self.ram.add_page(front)
            assert idx_in_RAM is not None

            self.table.set_present_in_RAM(front, idx_in_RAM)
            self.disk.delete_page(front)
            self._pages_in_RAM.append(front)
            cnt -= 1

        # adding all waiting pages allowed, if theres free space in ram it will be added there,
        # otherwise it will be added in disk
        while self._waiting_pages and cnt > 0:
            front = self.__get_and_delete_front_waiting_pages()
            idx_in_RAM = self.ram.add_page(front)
            self.table.add_page(front)
            # if theres not a valid page to add idx_in_RAM will be None
            if idx_in_RAM is not None:
                self.table.set_present_in_RAM(front, idx_in_RAM)
                self._pages_in_RAM.append(front)
            else:
                self.disk.add_page(front)
                self.table.set_not_present_in_RAM(front)
                self._pages_in_disk.append(front)
            cnt -= 1

    def execute(self):

        self.add_pages_in_waiting_pages_from_processes()

        self.delete_first_elements_from_pages_in_RAM()

        self.add_first_pages_to_RAM()

        print("----------------------------------------------------")
        self.ram.print()
        print("----------------------------------------------------")

        self.table.print()
        print("----------------------------------------------------")

        self.disk.print()
        print("----------------------------------------------------")

        self.check_state()
        print("pages in ram")
        for page in self._pages_in_RAM:
            print(page.associated_pid_process, page.process_index)
        print("----------------------------------------------------")
        print("pages in disk")
        for page in self._pages_in_disk:
            print(page.associated_pid_process, page.process_index)
        print("----------------------------------------------------")
        print("_waiting_pages")
        for page in self._waiting_pages:
            print(page.associated_pid_process, page.process_index)
        print("----------------------------------------------------")
        print("blocked_processes")
        for process in self.blocked_processes:
            print(process.pid)
        print("----------------------------------------------------")
        print("waiting_processes")
        for process in self.waiting_processes:
            print(process.pid)
        print("----------------------------------------------------")

        self.time += 1

class RP_FIFO(Replacing_Pages):

    def __init__(self, processes: Process, elements_per_time: int):
        super().__init__(processes, elements_per_time)

class RP_LRU(Replacing_Pages):

    def __init__(self, processes: Process, elements_per_time: int):
        super().__init__(processes, elements_per_time)

    # after running scheduling algorithm frequency of a page should be updated
    def update_pages_frequency_of_a_process(self, process: Process):
        for page in process.pages:
            self._pages_in_RAM.remove(page)
            self._pages_in_RAM.append(page)