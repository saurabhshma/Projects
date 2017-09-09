import Crypto
from Crypto.PublicKey import RSA
import rsa
import socket
import time
my_private_key = rsa.key.PrivateKey._load_pkcs1_pem(open('gen\\auth_private_key.pem','rb').read())

def request(req_key):
	private_key = rsa.key.PrivateKey._load_pkcs1_pem(open('gen\\auth_private_key.pem','rb').read())
	a_public_key = open('gen/'+req_key,'rb').read()
	sig = rsa.sign(a_public_key+req_key.encode(),private_key,'SHA-1')
	return (a_public_key,sig)
	
def get(req_key,public_key,sig):
	key = RSA.importKey(open('.\\gen\\auth_public_key.pem','rb').read())
	try:
		return rsa.verify(public_key+req_key.encode(),sig,key)
	except:
		return False
	
req_key = 'a_public_key.pem'
#request(req)
#exec(open('auth.py').read())

for i in range(10000000):
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	#socket.setdefaulttimeout(3)
	#print socket.getdefaulttimeout()
	port = 1234 
	s.bind((host, port))        # Bind to the port
	s.listen(1)                 # Now wait for client connection.
	#s.settimeout(30)
	c, addr = s.accept()
	req_key = rsa.decrypt(c.recv(1024),my_private_key).decode()
	
	curr_time = req_key[:10]
	req_key = req_key[10:]
	#print(curr_time,req_key)
	if(time.time()-int(curr_time)>5):
		print("Invalid Nonce")
	else:
		(public_key,sig) = request(req_key)
		c.send(sig)
		c.send(public_key)
	c.close()
	#print(time.time())