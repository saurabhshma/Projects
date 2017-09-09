import rsa
from Crypto import Random

rng = Random.new().read

(public_key,private_key) = rsa.newkeys(2048,rng)
file_out = open("auth_private_key.pem", "wb")
file_out.write(private_key._save_pkcs1_pem())
file_out.close()
file_out = open("auth_public_key.pem", "wb")
file_out.write(public_key._save_pkcs1_pem())
file_out.close()

(public_key,private_key) = rsa.newkeys(2048,rng)
file_out = open("a_private_key.pem", "wb")
file_out.write(private_key._save_pkcs1_pem())
file_out.close()
file_out = open("a_public_key.pem", "wb")
file_out.write(public_key._save_pkcs1_pem())
file_out.close()

(public_key,private_key) = rsa.newkeys(2048,rng)
file_out = open("b_private_key.pem", "wb")
file_out.write(private_key._save_pkcs1_pem())
file_out.close()
file_out = open("b_public_key.pem", "wb")
file_out.write(public_key._save_pkcs1_pem())
file_out.close()

