import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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


def etaisyysLaskuri(p1, p2):
    etaisyys = np.sqrt(np.power(p2[0]-p1[0],2)  + np.power(p2[1]-p1[1],2)  +  np.power(p2[2]-p1[2],2))
    return(etaisyys)