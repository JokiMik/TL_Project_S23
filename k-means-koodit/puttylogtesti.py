import numpy as np
import matplotlib.pyplot as plt
import utilities as sub

#Step 1 Datan lukeminen tiedostosta ja muuttaminen numpy matriisiksi
data = np.loadtxt('putty.log')
data = data.reshape(40,3)
#print(data)


#Step 2. Arvotaan keskipisteet
numberOfRows = data.shape[0]
numberOfCP = 4
maxValue = np.max(data)
centerPoints = np.random.randint(300, maxValue, size=(4, 3)) # 4kpl satunnaisia keskipisteitä väliltä 0-maxarvo
#print(centerPoints)

sub.plotData(data, centerPoints)

#Step 4. Lasketaan etäisyydet keskipisteistä pisteisiin
centerPointCumulativeSum = np.zeros((numberOfCP,3)) #
counts = np.zeros((1,numberOfCP)) # laskuri voittaville pisteille (eli mikä piste lähinnä mitäkin keskipistettä)
distances = np.zeros((1,numberOfCP)) # etäisyydet keskipisteistä pisteisiin

#Määritetään kuvaaja ennen opetusta
fig = plt.figure()

teachingRounds = 30

for kierros in range(teachingRounds):
    for i in range(0,numberOfRows):
        for j in range(0,numberOfCP):
            distances[0,j] = sub.etaisyysLaskuri(data[i,:],centerPoints[j,:]) # lasketaan jokaisen pisteen etäisyys keskipistee
        voittaja = np.argmin(distances) # tallennetaan voittavan keskipisteen indeksi
        
        '''
        if voittaja == 0:
            centerPointCumulativeSum[0,:] = centerPointCumulativeSum[0,:] + data[i,:] # lisätään piste keskipisteiden summaan
            counts[0,0] = counts[0,0] + 1 # lisätään laskuriin yksi
        elif voittaja == 1:
            centerPointCumulativeSum[1,:] = centerPointCumulativeSum[1,:] + data[i,:]
            counts[0,1] = counts[0,1] + 1
        elif voittaja == 2:
            centerPointCumulativeSum[2,:] = centerPointCumulativeSum[2,:] + data[i,:]
            counts[0,2] = counts[0,2] + 1
        elif voittaja == 3:
            centerPointCumulativeSum[3,:] = centerPointCumulativeSum[3,:] + data[i,:]
            counts[0,3] = counts[0,3] + 1
        '''
        
        for k in range(0,numberOfCP):
            if voittaja == k:
                centerPointCumulativeSum[k,:] = centerPointCumulativeSum[k,:] + data[i,:] #lisätään voittavan keskipisteen summaan voittava piste
                counts[0,k] = counts[0,k] + 1 #lisätään voittaneen keskipisteen laskuriin yksi

    #Step 5. Lasketaan uudet keskipisteet
    for i in range(0,numberOfCP):
        if counts[0,i] == 0:
            centerPoints[i,:] = np.random.randint(300, maxValue, size=(1, 3)) # jos keskipisteelle ei ole yhtään voittavaa pistettä, arvotaan uusi keskipiste
        else:
            centerPoints[i,:] = centerPointCumulativeSum[i,:] / counts[0,i] #päivitetään uusi keksipiste keskiarvolla (summa jaettuna laskurilla)
    
    # Tulosta kuvaaja jokaisen kierroksen jälkeen
    plt.clf()
    ax = fig.add_subplot(projection='3d')
    ax.set_title('Sensoridata 3D-avaruudessa')
    ax.set_xlabel('x-akseli')
    ax.set_ylabel('y-akseli')
    ax.set_zlabel('z-akseli')
    ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
    ax.scatter(centerPoints[:,0], centerPoints[:,1], centerPoints[:,2],c='blue',marker='X', s=100)
    plt.pause(0.1)
plt.show()
#print(centerPointCumulativeSum)
