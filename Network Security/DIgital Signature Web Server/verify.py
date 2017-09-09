import hashlib
import binascii
import slate
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import pyqrcode
import png
import qrtools
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject
import sys
import rsa

fileName = str(sys.argv[1]) 

def loadPubKey(filename):
	file = open(filename)
	temp = rsa.key.PublicKey._load_pkcs1_pem(file.read())
	file.close()
	return temp

pdf = PdfFileReader(open("uploads/"+fileName, 'rb'))
try:
	sign1 = pdf.getDocumentInfo()['/Sign1']
except:
	print "Error: Please upload signed PDF"
	sys.exit(0)

try:
	sign2 = pdf.getDocumentInfo()['/Sign2']
except:
	print "Error: Please upload signed PDF"
	sys.exit(0)

with open("uploads/"+fileName) as f:
		doc = slate.PDF(f)

SMessage = ''
for i in range(len(doc)):
	SMessage = SMessage + doc[i]

SMessage = binascii.hexlify(SMessage)

PublicKey1 = loadPubKey("keys/first_pub.pem")
PublicKey2 = loadPubKey("keys/second_pub.pem")
try:
	print (rsa.verify(SMessage, binascii.unhexlify(sign1), PublicKey1) & rsa.verify(SMessage, binascii.unhexlify(sign2), PublicKey2))
except:
	print "False"