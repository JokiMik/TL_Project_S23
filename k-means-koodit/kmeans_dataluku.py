import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utilities as ut

df = pd.read_csv('data.csv',sep=';')

print(df.head())

#Tulostetaan pelkät x,y,z arvot
print(df.iloc[:,6:9])

# Muutetaan pandas dataframe numpy matriisiksi
data = df.iloc[:,6:9].to_numpy()

# Tulostetaan pisteet 3D kuvaajaan
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_title('Sensoridata 3D-avaruudessa')
ax.set_xlabel('x-akseli')
ax.set_ylabel('y-akseli')
ax.set_zlabel('z-akseli')
ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
plt.show()

#print(data)
