import os
import numpy as np
from scipy import misc
from PIL import Image
from sklearn import svm
from sklearn.model_selection import cross_val_score
#***************read data from directories***************************

input_dir = "../lfw_easy"
img_arr = np.zeros((1,1850), dtype=int)
labels = np.zeros((1,1))
for item in os.listdir(input_dir):
	pathname = os.path.join(input_dir, item)
	if(os.path.isdir(pathname)):
		for img in os.listdir(pathname):
			path_img = os.path.join(pathname, img)
			#print(img)
			face = np.around(misc.imread(path_img,'L'))
			face=face.flatten()
			img_arr=np.vstack((img_arr,face))
			labels = np.vstack((labels,item))


img_arr = img_arr[1:,:]
labels = labels[1:]
#******************************************show avg image********************************
avg_img = np.mean(img_arr, axis=0)
avg_img_show = np.reshape(avg_img,(-1,37))
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
#************************show top five faces corresponding to principal components**********************

for i in range(5):
	tmp_p = prin_comp[:,i]-(prin_comp[:,i]).min()
	tmp_show = (np.around((tmp_p)* 255.0/tmp_p.max())).T
	tmp = np.reshape(tmp_show,(-1,37))
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
print("one vs one:",np.average(scores))

projNorm = (projection-np.mean(projection,axis=0))/np.std(projection,axis=0)
clf2 = svm.SVC(kernel='linear')
scores2 = cross_val_score(clf2, projNorm, labels, cv=10)	#for projected image
scores2 = scores2*100
print("one vs one:",np.average(scores2))

#*************************last part**************************************
n = input("enter face_id: ")
n = int(n)
p = np.loadtxt('projection/proj.txt')
new_img = p[n,:]
tmp = np.reshape((np.dot(new_img,prin_comp.T)+avg_img),(-1,37))
img = Image.fromarray(tmp)
img.convert('RGB').save('last/proj_im'+str(n)+'.png')
img.show()


tmp = np.reshape(img_arr[n,:],(-1,37))
tmp = np.uint8(tmp)
img = Image.fromarray(tmp)
img.convert('RGB').save('last/orig_im'+str(n)+'.png')
img.show()