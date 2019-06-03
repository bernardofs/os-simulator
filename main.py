from scheduling_algorithms import *
from replacing_pages_algorithms import *
from components import *

# arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 1, 2, 0, 0, 5), Process(3, 2, 3, 0, 0, 2)]
# arr = [Process(1, 0, 4, 0, 0, 5), Process(2, 0, 2, 3, 0, 1), Process(3, 0, 1, 2, 0, 1), Process(4, 0, 1, 1, 0, 3)]
# arr = [Process(1, 0, 3, 0, 0, 5), Process(2, 0, 3, 0, 0, 5)]
# arr = [Process(1, 0, 2, 4, 0, 1), Process(2, 0, 1, 0, 0, 1), Process(3, 0, 2, 2, 0, 4)]
arr = [Process(1, 0, 3, 0, 0, 3), Process(2, 1, 3, 0, 0, 4), Process(3,2 , 4, 0, 0, 3)]


def main():

    replacing_pages_algorithm = 'LRU'
    scheduling_algorithm = 'Round_Robin'

    print("start")
    # rp = RP_FIFO(arr, 2)
    # rp = RP_LRU(arr, 2)
    # f = FIFO()
    # f = SJF()
    # f = Round_Robin(2, 1)
    # f = EDF(2, 1)

    if replacing_pages_algorithm == 'FIFO':
        rp = RP_FIFO(arr, 2)
    if replacing_pages_algorithm == 'LRU':
        rp = RP_LRU(arr, 2)

    if scheduling_algorithm == 'FIFO':
        f = FIFO()
    elif scheduling_algorithm == 'SJF':
        f = SJF()
    elif scheduling_algorithm == 'Round_Robin':
        f = Round_Robin(2, 1)
    elif scheduling_algorithm == 'EDF':
        f = EDF(2, 1)

    t = 0

    while rp.there_is_processes() and t < 40:

        print("\n\n\n\n\n\n\n")

        print("t = ", t)

        rp.execute()

        process, finished = f.execute(rp.waiting_processes, t, rp.ram)
        if finished:
            rp.running_process_pid = -1
            print ('finished')
            rp.delete_process(process)
        else:
            if replacing_pages_algorithm == 'LRU':
                rp.update_pages_frequency_of_a_process(process) 

        t += 1


        rp.running_process_pid = process.pid
        print("rp.running_process_pid", rp.running_process_pid)
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")
        print("----------------------------------------------------")

    print ('TURNAROUND = ', f.turnaround / len(arr))


if __name__ == "__main__":
    main()
