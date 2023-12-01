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

a0 = np.array([1500,1500,1200]) # testidata
print('len w1 = ',len(w1))
print('shape a0',a0.shape)
print('shape w1',w1.shape)
print('shape b1',b1.shape)
print('shape w2',w2.shape)
print('shape b2',b2.shape)

a1 = relu(np.matmul(a0,w1) + b1) 
a2 = softmax(np.matmul(a1,w2) + b2) 

'''
matmul = np.matmul(a0,w1) 
print('Miltä matmul tulos näyttää',matmul)

c = np.zeros((w1.shape[1], 1))
for i in range(w1.shape[1]):  # Käydään läpi w1-matriisin sarakkeet
    for j in range(a0.shape[0]):  # Käydään läpi a0-matriisin rivit
        c[i] += a0[j] * w1[j][i]  # Lasketaan pistetulo ja päivitetään c-matriisi

c = c.reshape(10,)
print('testi',c)
toimiiko = relu(c + b1)
print('toimiiko',toimiiko)
'''

print("Neuroverkon tulos: ", np.argmax(a2))

# .h tiedostojen kirjoittaminen

def writeDataToHeaderFile(data, filename): 
    with open(filename+'.h', 'w') as f:
        f.write(f'#ifndef {filename}_H\n')
        f.write(f'#define {filename}_H\n')
        if len(data.shape) == 1:  # Tarkistetaan jos data on vektori
            f.write(f'const float {filename}[{data.shape[0]}] = {{')
            for i in range(data.shape[0]):
                f.write(str(data[i]))
                if i != data.shape[0]-1:
                    f.write(",")
        else:  # Jos data on matriisi
            f.write(f'const float {filename}[{data.shape[0]}][{data.shape[1]}] = {{')
            for i in range(data.shape[0]):
                f.write("{")
                for j in range(data.shape[1]):
                    f.write(str(data[i,j]))
                    if j != data.shape[1]-1:
                        f.write(",")
                f.write("},\n")
        f.write('};\n')
        f.write('#endif\n')

writeDataToHeaderFile(w1, 'W1')
writeDataToHeaderFile(b1, 'B1')
writeDataToHeaderFile(w2, 'W2')
writeDataToHeaderFile(b2, 'B2')