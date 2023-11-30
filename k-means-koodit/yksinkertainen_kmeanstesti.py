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
    counts[:] = 0 # laskurin nollaus
    centerPointCumulativeSum[:] = 0 # kumulatiivisen summan nollaus

    # Step 4. Lasketaan etäisyydet keskipisteistä kaikkiin pisteisiin
    for i in range(numberOfRows): # käydään läpi kaikki pisteet data matriisista
        for j in range(numberOfCP): # käydään läpi kaikki keskipisteet
            distances[:,j] = sub.etaisyysLaskuri(data[i,:],centerPoints) # lasketaan jokaisen pisteen etäisyys keskipisteen
        voittaja = np.argmin(distances) # tallennetaan voittavan keskipisteen indeksi
        
        # Step 5. Voittajan päivittäminen
        centerPointCumulativeSum[voittaja,:] = centerPointCumulativeSum[voittaja,:] + data[i,:] # lisätään voittavan keskipisteen kumulatiiviseen summaan voittava piste
        counts[:,voittaja] = counts[:,voittaja] + 1 # lisätään voittaneen keskipisteen laskuriin yksi

    # Step 6. Lasketaan uudet keskipisteet
    for i in range(numberOfCP):
        if counts[:,i] == 0:
            centerPoints = np.random.randint(800, maxValue, size=(1, 3)) # jos keskipisteelle ei ole yhtään voittavaa pistettä, arvotaan uusi keskipiste
        else:
            centerPoints = centerPointCumulativeSum[i,:] / counts[:,i] # päivitetään uusi keksipiste keskiarvolla (summa jaettuna laskurilla)
    

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_title('Sensoridata 3D-avaruudessa')
ax.set_xlabel('x-akseli')
ax.set_ylabel('y-akseli')
ax.set_zlabel('z-akseli')
ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
ax.scatter(centerPoints[0], centerPoints[1], centerPoints[2],c='blue',marker='X', s=100)
plt.show()
