from scheduling_algorithms import *
from replacing_pages_algorithms import RP_FIFO
from process import *

# arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 10, 2, 0, 0, 5), Process(3, 10, 3, 0, 0, 2)]
arr = [Process(1, 0, 4, 0, 0, 5), Process(2, 0, 2, 3, 0, 1), Process(3, 0, 1, 2, 0, 1), Process(4, 0, 1, 1, 0, 3)]


def main():

    print("start")
    rp = RP_FIFO(arr, 2)
    # f = FIFO()
    f = SJF()
    t = 0

    sort_arr = True
    while rp.there_is_processes() and t < 40:

        print("t = ", t)

        rp.execute()

        if sort_arr:
        	print ("\n\n\n\n\n\n\n SORTING \n\n\n\n\n\n\n")
        	rp.sort_waiting_processes_by_exec_time()
        	sort_arr = False

        process, finished = f.execute(rp.waiting_processes, t, rp.ram)
        if finished:
            rp.running_process_pid = -1
            rp.delete_process(process)
            sort_arr = True
        t += 1
        rp.running_process_pid = process.pid
        print("rp.running_process_pid", rp.running_process_pid)
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")


if __name__ == "__main__":
    main()
