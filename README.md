# Computer-Networks

## Group Members:

	Rahul R Shevade - 2017B3A70878H
	Kasam Vamshi - 2017B3A70740H
	Shanmukh Kaliprasad Padmanabhuni - 2017B3A71048H
	Pranav V Grandhi - 2017B2A71604H
	Suhas Reddy N - 2017B4A70885H
	Vashist SLN - 2017B3A70381H


This project is the implementation of a reliable UDP protocol with a file transfer layer above it. The file transfer protocol allows transferring filesof various types like gif, mp3, We used Selective Repeat Algorithm to ensure reliability. It is a better alternative to other approaches like Go-Back-N and Stop and wait, which involve unnecessary retransmissions and a significantly lowered bandwidth respectively.

The project has the following files:
	> client.py - Class encapsulating the functions of client (such as sending)
	> server.py - Class encapsulating server functions such as receiving.
	> data_packet.py - Consists of various functions such as checksum, jsonify, checksumVerification that allow easier ways to handle packets in server and clients.
	> test.py - Driver file.

How To Run
----------
> Note: The file that should be sent should be in the same directory as the sender. 
> Example for client : python3 test.py -c 127.0.0.1 12345 4 8888
 			
 			> -c indicates client mode
 			> 127.0.0.1 is the server IP (localhost in this example)
 			> 12345 is the server port
 			> 4 is the window size
 			> 8888 is the client port to send packets.


> Example for server: python3 test.py -s 127.0.0.1 12345
					
					> -s indicates server mode
					> 127.0.0.1 is server IP (Localhost here)
					> 12345 is server port.
> If you want to simulate packet loss, uncomment the randomizer in server.py file. 

Receiver's Algorithm
--------------------

> The receiver's role is to store the packets given by client and sending acknowledgements for the same.

> First, convert the JSON Dumps received into dictionary form.

> Verify that the packets sent remain uncorrupted by calculating the checksum of the data and comparing it with the checksum stored in the packet separately. This gives sufficient proof that the data is unalterered.

> If the packets are uncorrupted, send the ack corresponding to the packet to client. Check whether the packet sent is the expected packet or not.

> If the packet is the expected packet, append the pkt to the packet list and remove the next sequence of expected packets from the buffer if it's present in it.

> If the packet isn't the expected packet, add it to the buffer. The buffer represents packets that were received out of order.

> Sort the packet list according to numbers and write to file. 

> The "file_packet" carries the name of the file to the server so the type of file is properly identified.

> The bye packet signals the end of transfer. 

Sender's Algorithm
-------------------

>We have two threads running Ack and main
	>Ack thread listens to the ack's sent by the receiver
	>Main thread sends the packet to the receiver
	>We have 5 global variables shared commonly between both threads
		>buffer_ack	: Stores the ack values, incase if the ack are out of order 
		>current_ack	: Stores the latest correctly recvd ack
		>expected_ack	: The ack which we expect
		>packet_list	: This the initial packet list generated from the file
		>window_head	: Denotes the starting of the window.

	>In the main thread, 
		>We first convert the file into packets and store them in a list.
		> We also append two more packets, one containing the name of the file, two containing the closing packet.
		> We call the send function.
		> We then loop until the current_ack is greater than equal to the maximum packet number.
			> In the loop, we check if the distance between last packet sent and the last ack recvd is less than window size, then we send the increment the pkt_head.
			> If the packet's has been already sent successfully, we dont send it.
			> Else we send the packet.

	> In the Ack thread, we receive the acks,
		> If the ack is received with no corruption, we proceed.
		> When the ack received is equal to the ack expected.
			> We increment the ack received and expected
			> We also update the status of the the packet, since it's received successfully.
			> We then check for the ack buffer, and see if we have some out of order acks
			> If we have and they are in order with what we expect, then we update the ack received and ack expected
		    > When the ack received is greater than the ack expected, then that means it's out of order
			> We push it to the ack buffer
			> We update the status of the packet

	> We also run the timer, with a value of 0.7 seconds.
		>When we reach a time out, we put the paket head to the start of the window.
		> As a result in, the main thread, the packet head will move across the window and send the files, whose acks haven't been received yet.
