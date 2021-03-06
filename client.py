# Rahul R Shevade - 2017B3A70878H
# Kasam Vamshi - 2017B3A70740H
# Shanmukh Kaliprasad Padmanabhuni - 2017B3A71048H
# Pranav V Grandhi - 2017B2A71604H
# Suhas Reddy N - 2017B4A70885H
# Vashist SLN - 2017B3A70381H

import socket
import threading
import signal
import math
import time
import time
from data_packet import *
import os
import time

global window_head,current_ack, expected_ack, buffer_ack, lock, max_pkt_no, packet_list
window_head=-1
current_ack=-1
expected_ack=0
buffer_ack=[]
packet_list=[]
class client:

	def __init__ (self, server_IP, server_port, window, client_pkt_port):
		
		self.server_IP=server_IP
		self.server_port=server_port
		self.window=window
		self.pkt_port=client_pkt_port
		self.ack_port = client_pkt_port+5
		self.server_address= (server_IP,server_port)

		send_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		send_socket.bind(('', self.pkt_port))
		self.send_socket=send_socket

		ack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ack_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		ack_socket.bind(('', self.ack_port))
		self.ack_socket=ack_socket

	def run(self):
		global window_head,current_ack, expected_ack, buffer_ack, lock, packet_list
		while True:
			if(current_ack==max_pkt_no and not buffer_ack):
				# print("Bye Packet Received")
				return

			data, address = self.ack_socket.recvfrom(1024)
			data = json.loads(data.decode('utf-8'))
			if(check_ack(data)):
				with lock:
					ack_number = data['number']
					# print("before if",ack_number)
					if(ack_number>expected_ack and ack_number not in buffer_ack):
					    print("Out of order : ", ack_number)
					    buffer_ack.append(ack_number)
					    buffer_ack.sort()
					    temppkt=json.loads(packet_list[ack_number].decode('utf-8'))
					    temppkt['status']=True
					    packet_list[ack_number] = jsonify(temppkt['data'],temppkt['pkt_type'],temppkt['number'],temppkt['status'],temppkt['checksum'])

					elif(ack_number==expected_ack):
					    print(ack_number)
					    current_ack +=1
					    expected_ack +=1
					    temppkt=json.loads(packet_list[ack_number].decode('utf-8'))
					    temppkt['status']=True
					    packet_list[ack_number] = jsonify(temppkt['data'],temppkt['pkt_type'],temppkt['number'],temppkt['status'],temppkt['checksum'])
					    signal.setitimer(signal.ITIMER_REAL, 0.7)
					    print(buffer_ack)
					    while buffer_ack and buffer_ack[0]==expected_ack:
					        current_ack = expected_ack
					        expected_ack = buffer_ack[0] + 1
					        # print("Hi : ", current_ack)
					        buffer_ack.remove(buffer_ack[0]);
					        # print(buffer_ack)
					        buffer_ack.sort()

	def send(self,filename):
		fd= open(filename, 'rb')
		content= fd.read()
		global window_head,current_ack, expected_ack, buffer_ack, lock, max_pkt_no, packet_list
		packet_list=make_pktlist(content, filename)
		max_pkt_no = len(packet_list)-1
		# window_head=-1
		# current_ack=-1
		# expected_ack=0
		lock= threading.Lock()
		buffer_ack=[]

		def reset_head(self,signum):
		    # print("Hi")
		    global window_head,current_ack, expected_ack, buffer_ack, lock
		    if(current_ack<max_pkt_no):
		        # print("Hi Head")
		        window_head=current_ack
		    signal.setitimer(signal.ITIMER_REAL, 0.7)

		starttime= time.time()
		signal.signal(signal.SIGALRM, reset_head)
		ack_thread = threading.Thread(target=self.run)
		ack_thread.start()
		signal.setitimer(signal.ITIMER_REAL, 0.7)

		while current_ack < max_pkt_no:
			with lock:
				while (window_head - current_ack < self.window):
					window_head+=1
					if window_head>max_pkt_no:
						break
					curr_pkt= json.loads(packet_list[window_head].decode('utf-8'))
					if curr_pkt['status']== False:
						print("Sending Packet to Server: ", curr_pkt['number'])
						self.send_socket.sendto(packet_list[window_head],self.server_address)

		ack_thread.join()

		endtime=time.time()
		duration=abs(starttime-endtime)
		filesize=os.path.getsize(filename)
		throughput=filesize/duration
		print("duration: ",duration)
		print("filesize: ",filesize)
		print("throughput: ", throughput)

	