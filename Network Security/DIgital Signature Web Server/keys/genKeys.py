import rsa

def genKey(filename):
	(publicKey, privateKey) = rsa.newkeys(1024)
	filepub = open(filename + "_pub" + ".pem", "wb")
	filepriv = open(filename + "_priv" + ".pem", "wb")
	filepub.write(publicKey._save_pkcs1_pem())
	filepriv.write(privateKey._save_pkcs1_pem())
	filepub.close()
	filepriv.close()

genKey("first")
genKey("second")