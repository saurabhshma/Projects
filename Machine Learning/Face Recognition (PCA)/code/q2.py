import os
import numpy as np
from scipy import misc
from PIL import Image
from sklearn import svm
from sklearn.model_selection import cross_val_score
#***************read data from directories***************************

input_dir = "../orl_faces"
img_arr = np.zeros((1,10304), dtype=int)
labels = np.zeros((1,1))
for item in os.listdir(input_dir):
	pathname = os.path.join(input_dir, item)
	if(os.path.isdir(pathname)):
		for img in os.listdir(pathname):
			path_img = os.path.join(pathname, img)
			#print(img)
			face = misc.imread(path_img)
			face=face.flatten()
			img_arr=np.vstack((img_arr,face))
			labels = np.vstack((labels,item))

# XTrainGray = np.zeros((400, 10304), dtype=int)
# Ytrain = []
# path = '/media/shalini/New Volume/ubuntu/MTECH/sem2/ml/assignments/assgn4/q2/orl_faces'
# directoryContents = os.listdir(path)
# exampleNum = 0
# for i in directoryContents:
#     temp = i
#     if os.path.isdir(path+'/'+temp):
#         for j in os.listdir(path+'/'+i):
#             XTrainGray[exampleNum, :] = misc.imread(path+'/'+i+'/'+j).flatten()
#             Ytrain.append(temp)
#             exampleNum = exampleNum + 1

img_arr = img_arr[1:,:]
labels = labels[1:]
#******************************************show avg image********************************
avg_img = np.mean(img_arr, axis=0)
avg_img_show = np.reshape(avg_img,(-1,92))
img = Image.fromarray(avg_img_show)
img.convert('RGB').save('avg_img/avg.png')
img.show()
#********************************************perform svd**************************************
img_arr_zmean = img_arr-avg_img					#zero mean image
U, s, Vt=np.linalg.svd(img_arr_zmean)
V = Vt.T
#*******************************principal component matrix obtained************************
prin_comp = V[:,:50]
np.savetxt('principal_com/pc.txt',prin_comp)		#save principal component matrix
#b = np.loadtxt('principal_com/pc.txt')
tmp_p = (prin_comp-prin_comp.min())
prin_show = (np.around((tmp_p)* 255.0/tmp_p.max())).T 	#bring principal component matrix between 0-255

#************************show top five faces corresponding to principal components**********************
p_show = prin_show[:5,:]
for i in range(p_show.shape[0]):
	tmp = np.reshape(p_show[i,:],(-1,92))
	img = Image.fromarray(tmp)
	img.convert('RGB').save('prin_img/p'+str(i)+'.png')
	img.show()

projection = np.dot(img_arr_zmean,prin_comp)
np.savetxt('projection/proj.txt',projection)

#********************************SVM Classifier*****************************************
c, r = labels.shape
labels = labels.reshape(c,)
clf = svm.SVC(kernel='linear')
scores = cross_val_score(clf, img_arr, labels, cv=10)		#for original image
scores = scores*100
print("one vs one:",scores)

clf2 = svm.SVC(kernel='linear')
scores2 = cross_val_score(clf2, projection, labels, cv=10)	#for projected image
scores2 = scores2*100
print("one vs one:",scores2)

#*************************last part**************************************
n = input("enter face_id: ")
n = int(n)
p = np.loadtxt('projection/proj.txt')
tmp = np.reshape(p[n,:],(-1,92))
img = Image.fromarray(tmp)
img.show()


tmp = np.reshape(img_arr[n,:],(-1,92))
img = Image.fromarray(tmp)
img.show()