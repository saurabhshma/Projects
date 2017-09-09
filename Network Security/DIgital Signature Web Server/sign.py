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
#fileName = raw_input("Please enter filename: ")

fileName = str(sys.argv[1]) 
######Digitally Signing the PDF######

with open(fileName) as f:
		doc = slate.PDF(f)

message = ''
for i in range(len(doc)):
	message = message + doc[i]

print 'ooo lala lala'
#print message

message = binascii.hexlify(message)  #Extracted PDF contents and converted into hex format

hashMessage = hashlib.sha256(message).hexdigest() #Message Hash in hex string format

random_generator = Random.new().read
publicKey1 = RSA.generate(1024, random_generator) #Public key for decryption
privateKey1 = publicKey.publickey() #Private key for encryption

random_generator = Random.new().read
publicKey2 = RSA.generate(1024, random_generator) #Public key for decryption
privateKey2 = publicKey.publickey() #Private key for encryption

digitalSign1 = privateKey1.encrypt(hashMessage, 32)
digitalSign2 = privateKey2.encrypt(hashMessage, 32)
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
infoDict.update({NameObject('/Sign1'): createStringObject(binascii.hexlify(digitalSign1[0]))})
infoDict.update({NameObject('/Sign2'): createStringObject(binascii.hexlify(digitalSign2[0]))})
fout = open('signed.pdf', 'wb')
writer.write(fout)
fin.close()
fout.close()

pdf = PdfFileReader(open('signed.pdf', 'rb'))
sign = pdf.getDocumentInfo()['/Sign']
with open('signed.pdf') as f:
		doc = slate.PDF(f)

SMessage = ''
for i in range(len(doc)):
	SMessage = SMessage + doc[i]

SMessage = binascii.hexlify(SMessage)  #Extracted PDF contents and converted into hex format
sign = (binascii.unhexlify(sign),)
SHashMessage = hashlib.sha256(SMessage).hexdigest()
recvDigitalSign = publicKey.decrypt(ast.literal_eval(str(sign)))
#print recvDigitalSign == SHashMessage
