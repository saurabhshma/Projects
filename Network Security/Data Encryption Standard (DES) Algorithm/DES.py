import numpy as np;import _pickle as pic;(perm1,perm2,S,P,kperm1,kperm2,shifts)=pic.load(open('data.pic','rb'))

def print_data(data, x):
	for i in range(x):
		for j in range(8):
			print (data[i * 8 + j], end=" ")
		print()

def cycle(data,keyi):
	left,right,sbox=data[:32],data[32:],np.array([0]*32)
	'''
	print("data (Input to S-Box)")
	print_data(data, 8)
	'''
	#print("32-bit data (Input to F-Box)")
	#print_data(right, 4)
	#temp = (np.array([np.concatenate(([right[(i*4-1)%32]],right[i*4:(i+1)*4],[right[((i+1)*4)%32]])) for i in range(8)])).reshape([48])
	exor = np.bitwise_xor((np.array([np.concatenate(([right[(i*4-1)%32]],right[i*4:(i+1)*4],[right[((i+1)*4)%32]])) for i in range(8)])).reshape([48]),keyi)
	#print("Output from Expansion P-Box:")
	#print_data(temp, 6)
	#print("Output from XOR operation in S-box:")
	#print_data(exor, 6)

	for i in range(8):
		temp = S[i][exor[i*6]*32+exor[i*6+5]*16+exor[i*6+1]*8+exor[i*6+2]*4+exor[i*6+3]*2+exor[i*6+4]]
		sbox[i*4],sbox[i*4+1],sbox[i*4+2],sbox[i*4+3] = int((temp/8)%2),int((temp/4)%2),int((temp/2)%2),int(temp%2)
	return np.concatenate((right,np.bitwise_xor(left,sbox[P])))
def crypto(data,key,flag):
	key,keys,data = key[kperm1],[0]*16,data[perm1]
	C0,D0 = key[:28],key[28:]
	#print("data after initial permutation:")
	#print_data(data.tolist())

	#print("data after initial permutation: \n", print_data(data))
	for i in range(16):
		C0,D0 =  np.concatenate((C0[shifts[i]:],C0[:shifts[i]])),np.concatenate((D0[shifts[i]:],D0[:shifts[i]]))
		keys[i] = np.concatenate((C0,D0))[kperm2]
	for i in range(1,17): 
		data=cycle(data,keys[(17+(flag*i))%17-1])
		'''
		if(i == 1 and flag == 1):
			print("Encrypted data after round 1")
			print_data(data, 8)
		elif(i == 15 and flag == -1):
			print("Decrypted data after round 15")
			print_data(data, 8)
		'''
	return np.concatenate((data[32:],data[:32]))[perm2]

	
key = np.array([0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1])
data= np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1])

encrypt = crypto(data, key, 1)

decrypt = crypto(encrypt, key, -1)

print("initial data: ")
print_data(data, 8)
print()
print("encrypted data: ")
print_data(encrypt, 8)
print()
print("decrypted data: ")
print_data(decrypt, 8)


print()
print(crypto(crypto(data,key,1),key,-1)==data)
print_data(data)
print()
print_data()