#import hashlib
import binascii
import slate
#import Crypto
#from Crypto.PublicKey import RSA
#from Crypto import Random
#import ast
#import pyqrcode
#import png
#import qrtools
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject
import sys
import rsa
#fileName = raw_input("Please enter filename: ")

def loadPrivKey(filename):
	file = open(filename)
	temp = rsa.key.PrivateKey._load_pkcs1_pem(file.read())
	file.close()
	return temp


fileName = str(sys.argv[1]) 
######Digitally Signing the PDF######

with open(fileName) as f:
		doc = slate.PDF(f)

message = ''
for i in range(len(doc)):
	message = message + doc[i]

#print 'ooo lala lala'
#print message

message = binascii.hexlify(message)  #Extracted PDF contents and converted into hex format

privateKey1 = loadPrivKey("keys/first_priv.pem")
privateKey2 = loadPrivKey("keys/second_priv.pem")

digitalSign1 = rsa.sign(message, privateKey1, 'SHA-256')
digitalSign2 = rsa.sign(message, privateKey2, 'SHA-256')
#digitalSign = binascii.hexlify(digitalSign[0]) #Digital Signature in hex string format
#print digitalSign
###################
fin = file(fileName, 'rb')
pdf_in = PdfFileReader(fin)

writer = PdfFileWriter()

for page in range(pdf_in.getNumPages()):
    writer.addPage(pdf_in.getPage(page))

infoDict = writer._info.getObject()

info = pdf_in.documentInfo
for key in info:
    infoDict.update({NameObject(key): createStringObject(info[key])})

# add the grade
infoDict.update({NameObject('/Sign1'): createStringObject(binascii.hexlify(digitalSign1))})
infoDict.update({NameObject('/Sign2'): createStringObject(binascii.hexlify(digitalSign2))})
fout = open('signed.pdf', 'wb')
writer.write(fout)
fin.close()
fout.close()