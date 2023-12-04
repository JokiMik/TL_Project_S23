import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def relu(x):
	for i in range(len(x)):
		if x[i] < 0:
			x[i] = 0
	return x
	#return np.maximum(0, x)

def softmax(x):
	return(np.exp(x)/np.exp(x).sum())

w1 = np.loadtxt('w1.csv', delimiter=',')
w2 = np.loadtxt('w2.csv', delimiter=',')
b1 = np.loadtxt('b1.csv', delimiter=',')
b2 = np.loadtxt('b2.csv', delimiter=',')

a0 = np.array([1200,1500,1500]) # testidata
print('len w1 = ',len(w1))
print('shape a0',a0.shape)
print('shape w1',w1.shape)
print('shape b1',b1.shape)
print('shape w2',w2.shape)
print('shape b2',b2.shape)

a1 = relu(np.matmul(a0,w1) + b1) 
a2 = softmax(np.matmul(a1,w2) + b2) 


matmul = np.matmul(a0,w1) 
print('Miltä matmul tulos näyttää',matmul)


#Matriisikertolaskut for loopelilla c-kieltä varten
c1 = np.zeros((w1.shape[1],))
c2 = np.zeros((w2.shape[1],))
#c1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
c2 = [0, 0, 0, 0, 0, 0]
for i in range(w1.shape[1]):  # Käydään läpi w1-matriisin sarakkeet
    for j in range(a0.shape[0]):  # Käydään läpi a0-matriisin rivit
        c1[i] = c1[i] + a0[j] * w1[j][i]  # Lasketaan pistetulo ja päivitetään c-matriisi

print('c1 matmul tulos',c1)
c1 = relu(c1 + b1)
print('c1 relu',c1)

for i in range(w2.shape[1]): 
    for j in range(c1.shape[0]): 
        c2[i] = c2[i] + c1[j] * w2[j][i]  

c2 = softmax(c2 + b2)

print("Neuroverkon tulos (argmax a2): ", np.argmax(a2))
print("Neuroverkon tulos (todennäköisyys a2): ", a2)

print("Neuroverkon tulos (argmax c2): ", np.argmax(c2))
print("Neuroverkon tulos (todennäköisyys c2): ", c2)

# .h tiedoston kirjoittaminen

def writeDataToHeaderFile(data, filename, varname): 
    with open(filename+'.h', 'a') as f:
        if len(data.shape) == 1:  # tarkistus onko data vektori vai matriisi
            f.write(f'const float {varname}[{data.shape[0]}] = {{')
            for i in range(data.shape[0]):
                f.write(str(data[i]))
                if i != data.shape[0]-1:
                    f.write(",")
        else:  # jos data on matriisi
            f.write(f'const float {varname}[{data.shape[0]}][{data.shape[1]}] = {{')
            for i in range(data.shape[0]):
                f.write("{")
                for j in range(data.shape[1]):
                    f.write(str(data[i,j]))
                    if j != data.shape[1]-1:
                        f.write(",")
                f.write("},\n")
        f.write('};\n')

def writeWeightsToHeaderFile(w1, b1, w2, b2, filename):
    # Kirjoitetaan header-tiedostoon alkuosa
    with open(filename+'.h', 'w') as f:
        f.write(f'#ifndef {filename.upper()}_H\n')
        f.write(f'#define {filename.upper()}_H\n')
    # Lisätään tiedostoon painot ja biasit
    writeDataToHeaderFile(w1, filename, 'W1')
    writeDataToHeaderFile(b1, filename, 'B1')
    writeDataToHeaderFile(w2, filename, 'W2')
    writeDataToHeaderFile(b2, filename, 'B2')
    #lopuksi lisätään header-tiedostoon loppuosa
    with open(filename+'.h', 'a') as f:
        f.write('#endif\n')

#writeWeightsToHeaderFile(w1, b1, w2, b2, 'neuroverkonKertoimet')