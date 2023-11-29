import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import utilities as sub

#Step 1 Datan lukeminen tiedostosta ja muuttaminen numpy matriisiksi
df = pd.read_csv('data.csv',sep=';')

#print(df.head())

#Tulostetaan pelkät x,y,z arvot
#print(df.iloc[:,6:9])

# Muutetaan vain xyz sarakkeet numpy matriisiksi
data = df.iloc[:,6:9].to_numpy()


numberOfRows = data.shape[0] #rivien määrä eli x,y,z pisteiden määrä
numberOfCP = 6 
maxValue = np.max(data)
#Step 2. Arvotaan keskipisteet
centerPoints = np.random.randint(800, maxValue, size=(6, 3)) # 6kpl satunnaisia keskipisteitä väliltä 800-maxarvo
#print(centerPoints)

#Tulostetaan kuvaaja ennen opetusta
sub.plotData(data, centerPoints)

#Alustetaan tarvittavat muuttujat opetusta varten
centerPointCumulativeSum = np.zeros((numberOfCP,3)) #keksipisteiden kumulatiivinen summataulukko
counts = np.zeros((1,numberOfCP)) # laskuri voittaville pisteille (eli mikä piste lähinnä mitäkin keskipistettä)
distances = np.zeros((1,numberOfCP)) # etäisyydet keskipisteistä pisteisiin

#Määritetään kuvaaja ennen opetusta
fig = plt.figure()

teachingRounds = 100

for kierros in range(teachingRounds): #Step 7. Opetusta toistetaan riittävän monta kertaa
    #Step 4. Lasketaan etäisyydet keskipisteistä kaikkiin pisteisiin
    for i in range(0,numberOfRows): # käydään läpi kaikki pisteet data matriisista
        for j in range(0,numberOfCP): # käydään läpi kaikki keskipisteet
            distances[0,j] = sub.etaisyysLaskuri(data[i,:],centerPoints[j,:]) # lasketaan jokaisen pisteen etäisyys keskipisteen
        voittaja = np.argmin(distances) # tallennetaan voittavan keskipisteen indeksi
        
        #Step 5. Voittajan päivittäminen
        for k in range(0,numberOfCP): #päivitetään kumulatiivista summa muuttujaa ja laskuria
            if voittaja == k:
                centerPointCumulativeSum[k,:] = centerPointCumulativeSum[k,:] + data[i,:] #lisätään voittavan keskipisteen kumulatiiviseen summaan voittava piste
                counts[0,k] = counts[0,k] + 1 #lisätään voittaneen keskipisteen laskuriin yksi

    #Step 6. Lasketaan uudet keskipisteet
    for i in range(0,numberOfCP):
        if counts[0,i] == 0:
            centerPoints[i,:] = np.random.randint(800, maxValue, size=(1, 3)) # jos keskipisteelle ei ole yhtään voittavaa pistettä, arvotaan uusi keskipiste
        else:
            centerPoints[i,:] = centerPointCumulativeSum[i,:] / counts[0,i] #päivitetään uusi keksipiste keskiarvolla (summa jaettuna laskurilla)
    
    # Tulosta kuvaaja jokaisen kierroksen jälkeen
    plt.clf() # tyhjennetään kuvaaja
    ax = fig.add_subplot(projection='3d')
    ax.set_title('Sensoridata 3D-avaruudessa')
    ax.set_xlabel('x-akseli')
    ax.set_ylabel('y-akseli')
    ax.set_zlabel('z-akseli')
    ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
    ax.scatter(centerPoints[:,0], centerPoints[:,1], centerPoints[:,2],c='blue',marker='X', s=100)
    plt.pause(0.1)
plt.show()


#Step 8. Keksipisteiden tallennus kmeans.h tiedostoon        
sub.printCenterPoints("kmeans.h",centerPoints,numberOfCP)