import numpy as np
import matplotlib.pyplot as plt
import utilities as sub

data = np.zeros(9).reshape(3,3)

data[0,:] = 1
data[1,:] = 2
data[2,:] = 3

centerPoints = np.array([4,6,7])
#Step 2. Arvotaan keskipisteet
numberOfRows = data.shape[0]
numberOfCP = 1
maxValue = np.max(data)

#centerPoints = np.random.randint(200, maxValue, size=(4, 3)) # 4kpl satunnaisia keskipisteitä väliltä 0-maxarvo
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
ax.scatter(centerPoints[0], centerPoints[1], centerPoints[2],c='blue')
plt.show()

#Laskee etäisyydet keskipisteistä pisteisiin

teachingRounds = 1

for kierros in range(teachingRounds):
    for i in range(0,numberOfRows):
        for j in range(0,numberOfCP):
            distances[0,j] = sub.etaisyysLaskuri(data[i,:],centerPoints) # lasketaan jokaisen pisteen etäisyys keskipisteeseen
            print("distance = ",distances[0,j])
        voittaja = np.argmin(distances) # tallennetaan voittavan keskipisteen indeksi
        print("voittaja = ",voittaja)
        
        for k in range(0,numberOfCP):
            if voittaja == k:
                centerPointCumulativeSum[k,:] = centerPointCumulativeSum[k,:] + data[i,:] #lisätään voittavan keskipisteen summaan voittava piste
                counts[0,k] = counts[0,k] + 1 #lisätään voittaneen keskipisteen laskuriin yksi
                print("centerPointCumulativeSum = ",centerPointCumulativeSum[k,:])
    
    #Step 5. Lasketaan uudet keskipisteet
    for i in range(0,numberOfCP):
        centerPoints = centerPointCumulativeSum[i,:] / counts[0,i] #keskiarvo (summa jaettuna laskurilla)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_title('Sensoridata 3D-avaruudessa')
ax.set_xlabel('x-akseli')
ax.set_ylabel('y-akseli')
ax.set_zlabel('z-akseli')
ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
ax.scatter(centerPoints[0], centerPoints[1], centerPoints[2],c='blue',marker='X', s=100)
plt.show()
