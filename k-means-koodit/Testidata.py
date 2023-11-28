import numpy as np
import matplotlib.pyplot as plt

#Testidatan tekeminen xyz arvoille. Jokaisella suunnalla on 2 eri arvoa 1 pieni ja 10 iso  
data = np.zeros(36).reshape(12,3)

data[0:2,0] = 1 #x-suunta pieni arvo
data[2:4,0] = 10 #x-suunta iso arvo
data[4:6,1] = 1 #y-suunta pieni arvo
data[6:8,1] = 10 #y-suunta iso arvo
data[8:10,2] = 1  #z-suunta pieni arvo
data[10:12,2] = 10 #z-suunta iso arvo

#Step 2. Arvotaan keskipisteet
numberOfRows = data.shape[0]
numberOfCP = 1
maxValue = np.max(data)
centerPoints = np.random.randint(200, maxValue, size=(4, 3)) # 4kpl satunnaisia keskipisteitä väliltä 0-maxarvo
print(centerPoints)


#Step 4. Lasketaan etäisyydet keskipisteistä pisteisiin
centerPointCumulativeSum = np.zeros((numberOfCP,3)) #
counts = np.zeros((1,numberOfCP)) # laskuri voittaville pisteille (eli mikä piste lähinnä mitäkin keskipistettä)
distances = np.zeros((1,numberOfCP)) # etäisyydet keskipisteistä pisteisiin
# Tulostetaan pisteet 3D kuvaajaan
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_title('Sensoridata 3D-avaruudessa')
ax.set_xlabel('x-akseli')
ax.set_ylabel('y-akseli')
ax.set_zlabel('z-akseli')
ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
plt.show()



#Step 2. Arvotaan 6kpl satunnaisia keskipisteitä
arvotut_keskipisteet = np.random.randint(0,12,6)



# Step 3. Käydään läpi kaikki pisteet ja lasketaan niiden etäisyydet toisiinsa

def etaisyysLaskuri(p1, p2):
    etaisyys = np.sqrt(np.power(p2[0]-p1[0],2)  + np.power(p2[1]-p1[1],2)  +  np.power(p2[2]-p1[2],2))
    return(etaisyys)

for i in range(0,12):
    for j in range(0,12):
        etaisyys = etaisyysLaskuri(data[i,:],data[j,:])
        print("Pisteiden ",i," ja ",j," etäisyys on ",etaisyys)