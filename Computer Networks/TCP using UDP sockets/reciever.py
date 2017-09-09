import socket               # Import socket module
import sys
import select
import time
import random
import argparse
parser = argparse.ArgumentParser()

UDP_IP = str(sys.argv[1])	
UDP_PORT = int(sys.argv[2])

ack = 0
arr = [(0,0,0)]*10000
maxSize = -1

def checkArrayEmpty():             #check if buffer array is empty
	global arr
	if(arr[0] == 0):
		return True
	else:
		return False

def decode_data(data):             #Decode the data recieved
	s_no=int(data[0:6])      
	data_len=int(data[6:10])
	data=data[10:]
	return (s_no,data_len,data)

def addtoArray(temp):              #add packet into the buffer array
	key = decode_data(temp)
	global arr
	global maxSize
	if(checkArrayEmpty()):
		arr[0] = key
	else:
		i = maxSize
		while i >= 0 and arr[i] > key:
			arr[i + 1] = arr[i]
			i = i - 1
		arr[i + 1] = key

	maxSize = maxSize + 1

sock = socket.socket(socket.AF_INET, 
                     socket.SOCK_DGRAM)             #create socket for connection

sock.bind((UDP_IP, UDP_PORT))                        #bind the created socket

while True:
  data, addr = sock.recvfrom(1024)                  #Waiting to recieve packet from reciever
  temp = decode_data(data)                           #decode recieved packet
  s_no = temp[0]
  data_len = temp[1]
  print("sno", s_no)
  print("data_len", data_len)
  if(s_no == ack):                                   #check if recieved packet's sequence no. is equal to expected sequence number
    if checkArrayEmpty():                            #check if buffered array is empty or not
      ack = ack + data_len                           #calculate the acknowledgement number if buffer is empty
    else:                                            
      ack = ack + data_len
      while(arr[0][0] == int(ack)):
        ack = int(arr[0][0]) + int(arr[0][1])       #calculate the acknowledgement number if buffer is not empty
        arr = arr[1:]
        maxSize = maxSize - 1
  elif(s_no>ack):
  	addtoArray(data)                                 #add the packet to buffer if it is not equal to expected packet sequence number
  print("Ack", ack)
  sock.sendto(str(ack).encode(), addr)
sock.close()