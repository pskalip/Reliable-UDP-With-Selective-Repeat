# Rahul R Shevade - 2017B3A70878H
# Kasam Vamshi - 2017B3A70740H
# Shanmukh Kaliprasad Padmanabhuni - 2017B3A71048H
# Pranav V Grandhi - 2017B2A71604H
# Suhas Reddy N - 2017B4A70885H
# Vashist SLN - 2017B3A70381H


from server import *
from data_packet import *
from client import *
import sys


if __name__=="__main__":
	arguments= len(sys.argv)
	print(arguments)
	if(sys.argv[1]=="-c"):
		print("Client Mode: ON")
		c=client(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
		filename= input("Enter File Name:")
		c.send(filename)

	elif(sys.argv[1]=="-s"):
		print("Server Mode: ON")
		# for i in sys.argv:
		# 	print(i)
		s=server(sys.argv[2],int(sys.argv[3]))
		s.receive()
		print("FILE RECEIVED")
