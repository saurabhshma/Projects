import socket
import rsa
import Crypto
import sys
import select
import time
import random as rd
from Crypto.PublicKey import RSA

rd.seed(0)
host_s = '10.237.27.68'
myID = 'a'
my_private_key = rsa.key.PrivateKey._load_pkcs1_pem(open('gen/'+myID+'_private_key.pem','rb').read())
bID = 'b'
host_b = 'localhost'

	
def verify(req_key,public_key,sig):
	key = RSA.importKey(open('gen/auth_public_key.pem','rb').read())
	try:
		return rsa.verify(public_key+req_key.encode(),sig,key)
	except:
		return False

def get(req_key):
	key = RSA.importKey(open('gen/auth_public_key.pem','rb').read())
	s = socket.socket()
	port = 1234
	s.settimeout(3)
	s.connect((host_s,port))
	req_key = str(int(time.time())) + req_key
	s.send(rsa.encrypt(req_key.encode(),key))
	sig = s.recv(256)
	public_key = s.recv(1024)
	s.close()
	return (public_key,sig)

	
req_key = bID+'_public_key.pem'
public_key,sig = get(req_key)
print(time.time())
print(verify(req_key,public_key,sig))
b_public_key = rsa.key.PublicKey._load_pkcs1_pem(public_key)


s = socket.socket()
port = 1234
s.settimeout(3)
s.connect((host_b,port))

nonce1 = rd.random()
while(nonce1<0.11):
	nonce1 = rd.random()
nonce1 = str(int(nonce1*(10**10)))
print("nonce",nonce1+myID)
s.send(rsa.encrypt((nonce1+myID).encode(),b_public_key))
data = rsa.decrypt(s.recv(1024),my_private_key).decode()
r_nonce1 = data[10:]
nonce2 = data[10:]


loop = True
if(nonce1!=nonce1):
	print("nonce incorrect")
	loop=False
else:
	s.send(rsa.encrypt((nonce2).encode(),b_public_key))



while(loop):
	socket_list = [sys.stdin, s]
	read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
	for sock in read_sockets:
		if(sock==s):
			data = rsa.decrypt(s.recv(1024),my_private_key).decode()
			#data=s.recv(1024).decode()
			if(data=='quit'):
				print("---------------Quitting")
				loop=False
				break
			if(len(data)>0):
				print(data)
			#if not data:
				#print ("Disconnected!")
				#loop=False
				#break
		else:
			msg = input()
			if(msg=='quit'):
				s.send(rsa.encrypt('quit'.encode(),b_public_key))
				#s.send('quit'.encode())
				print("---------------Quitting")
				loop=False
				break
			else:
				s.send(rsa.encrypt(msg.encode(),b_public_key))
				#s.send(msg.encode())

				
s.close()