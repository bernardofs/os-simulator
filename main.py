from scheduling_algorithms import FIFO 
from replacing_pages_algorithms import RP_FIFO 
from process import *

arr = [Process(1,0,3,0,0,3), Process(2,5,2,0,0,5), Process(3,5,3,0,0,2)]

def main():

	print ('start')
	rp = RP_FIFO(arr, 2)
	f = FIFO()


	t = 0

	while(rp.there_is_processes and t < 20):

		print ('t = ', t)


		rp.execute()
		
		process, finished = f.execute(rp.waiting_processes, t, rp.ram)
		if finished:
			rp.running_process_pid = -1
			rp.delete_process(process)
		t += 1
		rp.running_process_pid = process.pid
		print ('rp.running_process_pid', rp.running_process_pid)
		print ('\n\n\n\n')

if __name__ == '__main__':
	main()