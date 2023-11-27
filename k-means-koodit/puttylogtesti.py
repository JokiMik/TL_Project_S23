import numpy as np
import matplotlib.pyplot as plt

#Step 1 Datan lukeminen tiedostosta ja muuttaminen numpy matriisiksi
data = np.loadtxt('putty.log')
data = data.reshape(40,3)
print(data)


#Step 2. Arvotaan keskipisteet
rivienlkm = data.shape[0]
maxarvo = np.max(data)

arvotut_keskipisteet = np.random.randint(0, maxarvo, size=(4, 3)) # 4kpl satunnaisia keskipisteitä väliltä 0-maxarvo
print(arvotut_keskipisteet)

# Tulostetaan pisteet 3D kuvaajaan
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_title('Sensoridata 3D-avaruudessa')
ax.set_xlabel('x-akseli')
ax.set_ylabel('y-akseli')
ax.set_zlabel('z-akseli')
ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
ax.scatter(arvotut_keskipisteet[:,0], arvotut_keskipisteet[:,1], arvotut_keskipisteet[:,2],c='blue')
plt.show()

#Step 3. Lasketaan etäisyydet keskipisteistä pisteisiin
def etaisyysLaskuri(p1, p2):
    etaisyys = np.sqrt(np.power(p2[0]-p1[0],2)  + np.power(p2[1]-p1[1],2)  +  np.power(p2[2]-p1[2],2))
    return(etaisyys)

etaisyydet = np.zeros((rivienlkm,4)) # 40 riviä ja 4 saraketta