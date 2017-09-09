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
myID = 'b'
my_private_key = rsa.key.PrivateKey._load_pkcs1_pem(open('gen/'+myID+'_private_key.pem','rb').read())

host_b = '10.194.55.154'


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

s = socket.socket()		 # Create a socket object
#socket.setdefaulttimeout(3)
#print socket.getdefaulttimeout()
port = 1234
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host_b, port))		# Bind to the port

s.listen(1)				 # Now wait for client connection.
s.settimeout(30)
c, addr = s.accept()
cliID=rsa.decrypt(c.recv(1024),my_private_key).decode()
print("cli",cliID)
nonce1 = cliID[:10]
cliID = cliID[10:]
#c.send('hello'.encode())

req_key = cliID+'_public_key.pem'
public_key,sig = get(req_key)
a_public_key = rsa.key.PublicKey._load_pkcs1_pem(public_key)
print(verify(req_key,public_key,sig))


nonce2 = rd.random()
while(nonce2<0.11):
	nonce2 = rd.random()
nonce2 = str(int(nonce2*(10**10)))
c.send(rsa.encrypt((nonce1+nonce2).encode(),a_public_key))
r_nonce2 = rsa.decrypt(c.recv(1024),my_private_key).decode()

loop=True
if(nonce2!=r_nonce2):
	print("nonce incorrect")
	loop=False



while(loop):
	socket_list = [sys.stdin, c]
	read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
	for sock in read_sockets:
		if(sock==c):
			data = rsa.decrypt(c.recv(1024),my_private_key).decode()
			#data = c.recv(1024).decode()            
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
				c.send(rsa.encrypt('quit'.encode(),a_public_key))
				#c.send('quit'.encode())
				print("---------------Quitting")
				loop=False
				break
			else:
				c.send(rsa.encrypt(msg.encode(),a_public_key))
				#c.send(msg.encode())
