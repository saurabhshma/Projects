import socket               # Import socket module
import sys
import select
import time
import random
import argparse
parser = argparse.ArgumentParser()
def encode_data(data,s_no):																	# Adding the headers to data
	s_no=str(s_no)
	while(len(s_no)<6):
		s_no='0'+s_no
	data_len=str(len(data))
	while(len(data_len)<4):
		data_len = '0'+data_len
	return s_no+data_len+data

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)											# Creating the UDP socket



'''
host = '10.192.33.240'
port = 12346
x=True
'''
host=str(sys.argv[1])																		# Taking arguments for host and port
port=int(sys.argv[2])
flag=str(sys.argv[3])
if(flag=='1'):
	x=False
else:
	x=True




addr = (host,port)
time_now=time.time()
time_start=time.time()
W=1000
conj_size=0
packs=[]
curr_sno=0
pack_len=0
start_pack_no=0
sr_no=0

print('Connected to server')
loop=True
while(start_pack_no<100000):
	#print(curr_sno)
	if(conj_size<W and W-conj_size>=1000): 															#creating packet of size 1000
		while(W-conj_size>=1000):
			packs.append(encode_data('0'*1000,curr_sno))
			curr_sno=curr_sno+1000																	
			pack_len=pack_len+1
			conj_size=conj_size+1000
			if(x or (random.random()*100>5)):
				s.sendto(packs[pack_len-1].encode(),addr)											# Sending the newly created packet
			print("Sent 1","seq_no_sent",curr_sno-1000,"W",W,"time",time.time()-time_start,"start pack",start_pack_no)
	

	if(conj_size<W and 0<=W-conj_size<1000): 														# Creating remaining size packet
		packs.append(encode_data('0'*(W-conj_size),curr_sno))
		temp=curr_sno
		curr_sno=curr_sno+W-conj_size
		pack_len=pack_len+1
		conj_size=W
		if(x or (random.random()*100>5)):															# Dropping packet with 0.05 probability
			s.sendto(packs[pack_len-1].encode(),addr)
		print("Sent 3","seq_no_sent",temp,"W",W,"time",time.time()-time_start,"start pack",start_pack_no)
	

	if(time_now+1<time.time()):																		# Checking for time out
		time_now=time.time()
		W=1000																						# Resetting W
		print("TIME OUT!!!!!!!!!!!!!!!!!!!!!")
		if(x or (random.random()*100>5)):
			s.sendto(packs[0].encode(),addr)
		print("Sent 3","seq_no_sent",int(packs[0][0:6]),"W",W,"time",time.time()-time_start,"start pack",start_pack_no) # Resending packet 0

	socket_list = [s]
	read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [],0)				# Checking if data is available in the socket

	temp=sr_no
	sr_no=""
	while(len(read_sockets)>0):
		sr_no=(s.recvfrom(1024)[0].decode())														# Getitng the latest ACK
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [],0)
		time_now=time.time()

	if(sr_no!=""):																					# Checking for incoming ACK
		print("Recieved 4","ACK",sr_no,"W",W,"time",time.time()-time_start,"start pack",start_pack_no)
		sr_no=int(sr_no)
		if(sr_no!=temp):
			W=W+int((1000000/W))																	# Increasoing W
		while(sr_no-start_pack_no>0):
			start_pack_no=start_pack_no+len(packs[0])-10
			conj_size=conj_size-len(packs[0])+10
			packs=packs[1:]
		pack_len=len(packs)
		
		if(pack_len!=0):
			if(x or (random.random()*100>5)):
				s.sendto(packs[0].encode(),addr)
				print("Sent 4","seq_no_sent",int(packs[0][0:6]),"W",W,"time",time.time()-time_start,"start pack",start_pack_no)  # Sending asked packet
s.close()

