class Page:
    def __init__(self, associated_pid_process: int, process_index: int):
        self.associated_pid_process = associated_pid_process
        self.process_index = process_index

    def __eq__(self, other):
        if not isinstance(other, Page):
            return NotImplemented

        return (
            self.associated_pid_process == other.associated_pid_process
            and self.process_index == other.process_index
        )


class Table:

    # - if pid is equal to -1 in an index of the table, then this index is empty
    # - table initializes empty
    def __init__(self, table_size: int):
        self.pages = [Page(-1, -1)] * table_size
        # if its -1, there's no element, if it's 0 it's on disk, if it's 1 it's on RAM
        self.present = [-1] * table_size
        self.index_in_RAM = [-1] * table_size
        self.ptr = 0

    def get_index(self, page: Page) -> int:
        for i, page_in_list in enumerate(self.pages):
            if page == page_in_list:
                return i
        return None

    def add_page(self, page: Page):
        self.pages[self.ptr] = page
        self.present[self.ptr] = 0
        self.index_in_RAM[self.ptr] = -1
        self.ptr = (self.ptr + 1) % len(self.pages)

    def set_not_present_in_RAM(self, page: Page):
        idx = self.get_index(page)
        self.present[idx] = 0
        self.index_in_RAM[idx] = -1

    def set_present_in_RAM(self, page: Page, index_in_RAM: int):
        idx = self.get_index(page)
        self.present[idx] = 1
        self.index_in_RAM[idx] = index_in_RAM

    def delete_page(self, page: Page):
        for i, page_in_list in enumerate(self.pages):
            if page_in_list == page:
                self.pages[i] = Page(-1, -1)
                self.present[i] = -1
                return

    def print(self):
        print("TABLE")
        for i, page in enumerate(self.pages):
            print(
                "page.pid = ",
                page.associated_pid_process,
                "page.process_index",
                page.process_index,
            )
        print("")


class Process:
    def __init__(
        self,
        pid: int,
        arrival_time: int,
        exec_time: int,
        deadline: int,
        priority: int,
        number_of_pages: int,
    ):
        self.pid = pid
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.deadline = deadline
        self.priority = priority
        self.pages = [Page(pid, i) for i in range(number_of_pages)]
        self.pages_in_RAM = 0

    # checks whether the process is ready to execute
    # returns false if it is blocked
    def is_ready(self) -> bool:
        return self.pages_in_RAM == len(self.pages)

    def get_number_of_pages(self):
        return len(self.pages)


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

    def print(self):
        print("DISK")
        for page in self.pages:
            print(page.associated_pid_process, page.process_index)
        print("")


class RAM:

    # - if pid is equal to -1 in an index of the RAM, then this index is empty
    # - RAM initializes empty
    def __init__(self, RAM_size: int):
        self.pages = [Page(-1, -1)] * RAM_size
        # a page should be executed at least one time to be deleted
        self.last_valid_pages = [Page(-1, -1)] * RAM_size
        self.executed = [False] * RAM_size
        self.RAM_size = RAM_size

    def get_index(self, page: Page) -> int:
        for i, page_in_list in enumerate(self.pages):
            if page == page_in_list:
                return i
        # if item is not found it returns -1
        return None

    def set_executed(self, page: Page):
        idx = self.get_index(page)
        self.executed[idx] = True

    def print(self):
        print("RAM")
        for page in self.last_valid_pages:
            print(page.associated_pid_process, page.process_index)
        print(self.executed)
        print(self.RAM_size)
        print("")

    def get_first_empty_page(self):
        for i, page in enumerate(self.pages):
            if page.associated_pid_process == -1:
                return i
        # if there isn't a page in RAM to be replaced
        return None

    def was_executed(self, page: Page):
        for i, page_in_list in enumerate(self.pages):
            if page_in_list == page:
                return self.executed[i]

        assert False

    def add_page(self, page: Page):
        RAM_idx = self.get_first_empty_page()
        if RAM_idx is None:
            return None
        self.pages[RAM_idx] = page
        self.last_valid_pages[RAM_idx] = page
        self.executed[RAM_idx] = False
        return RAM_idx

    def delete_page(self, page: Page):

        print("deleting: ", page.associated_pid_process, page.process_index)

        idx = self.get_index(page)
        if idx is None:
            return

        self.pages[idx] = Page(-1, -1)
        self.executed[idx] = False
