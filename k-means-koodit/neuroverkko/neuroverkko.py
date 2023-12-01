import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def relu(x):
	return np.maximum(0, x)
	'''
	if(x < 0):
		return 0                            # relu aktivaatio palauttaa aina nollan jos luku on negatiivinen, muuten x:än
	else:
		return x
	'''

def softmax(x):
	e_x = np.exp(x - np.max(x))  # vähennä maksimi estääksesi ylivuodon #return(np.exp(x)/np.exp(x).sum())
	return e_x / e_x.sum(axis=0)  # jaa jokainen elementti summan mukaan

w1 = np.loadtxt('w1.csv', delimiter=',')
w2 = np.loadtxt('w2.csv', delimiter=',')
b1 = np.loadtxt('b1.csv', delimiter=',')
b2 = np.loadtxt('b2.csv', delimiter=',')

a0 = np.array([1500,1500,1800]) # testidata
print(a0.shape)
print(w1.shape)
print(b1.shape)
print(w2.shape)
print(b2.shape)

a1 = relu(np.matmul(a0,w1) + b1) 
a2 = softmax(np.matmul(a1,w2) + b2) 

print("Neuroverkon tulos: ", np.argmax(a2))
