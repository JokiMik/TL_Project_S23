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
#data = data[0:112,:] # otetaan vain 112 ensimmäistä riviä, joissa sensoria pidetty paikallaan joka suunnassa

numberOfRows = data.shape[0] #rivien määrä eli x,y,z pisteiden määrä
numberOfCP = 6 
maxValue = np.max(data)
#Step 2. Arvotaan keskipisteet
centerPoints = np.random.randint(800, maxValue, size=(6, 3)) # 6kpl satunnaisia keskipisteitä väliltä 800-maxarvo
#print(centerPoints)

#Tulostetaan kuvaaja ennen opetusta
sub.plotData(data, centerPoints)

# Alustetaan tarvittavat muuttujat opetusta varten
centerPointCumulativeSum = np.zeros((numberOfCP,3)) # keksipisteiden kumulatiivinen summataulukko
counts = np.zeros((1,numberOfCP)) # laskuri voittaville pisteille (eli mikä piste lähinnä mitäkin keskipistettä)
distances = np.zeros((1,numberOfCP)) # etäisyydet keskipisteistä pisteisiin

# Määritetään kuvaaja ennen opetusta
fig = plt.figure()

teachingRounds = 50

for kierros in range(teachingRounds): # Step 7. Opetusta toistetaan riittävän monta kertaa
    counts[:] = 0 # laskurin nollaus
    centerPointCumulativeSum[:] = 0 # kumulatiivisen summan nollaus

    # Step 4. Lasketaan etäisyydet keskipisteistä kaikkiin pisteisiin
    for i in range(numberOfRows):
        for j in range(numberOfCP):
            distances[:,j] = sub.etaisyysLaskuri(data[i,:],centerPoints[j,:]) # lasketaan jokaisen pisteen etäisyys keskipisteen
        voittaja = np.argmin(distances) # tallennetaan voittavan keskipisteen indeksi

        # Step 5. Voittajan päivittäminen
        centerPointCumulativeSum[voittaja,:] = centerPointCumulativeSum[voittaja,:] + data[i,:] # lisätään voittavan keskipisteen kumulatiiviseen summaan voittava piste
        counts[:,voittaja] = counts[:,voittaja] + 1 # lisätään voittaneen keskipisteen laskuriin yksi
    
    # Step 6. Lasketaan uudet keskipisteet
    for i in range(numberOfCP):
        if counts[:,i] == 0: # jos keskipisteelle ei ole yhtään voittavaa pistettä, arvotaan uusi keskipiste
            centerPoints[i,:] = np.random.randint(800, maxValue, size=(1, 3)) 
        else:
            centerPoints[i,:] = centerPointCumulativeSum[i,:] / counts[:,i] # päivitetään uusi keksipiste keskiarvolla (summa jaettuna laskurilla)
    
    #print("Keskipisteet kierroksen ",kierros," jälkeen: ",centerPoints)
    #print("Laskurit kierroksen ",kierros," jälkeen: ",counts)

    # Päivitetään kuvaajaan uudet keskipisteet
    plt.clf() # tyhjennetään kuvaaja
    ax = fig.add_subplot(111,projection='3d')
    ax.set_title(f'Sensoridata 3D-avaruudessa\nOpetuskertoja: {kierros+1}/{teachingRounds}')
    ax.set_xlabel('x-akseli')
    ax.set_ylabel('y-akseli')
    ax.set_zlabel('z-akseli')
    ax.scatter(data[:,0], data[:,1], data[:,2], c='red')
    ax.scatter(centerPoints[:,0], centerPoints[:,1], centerPoints[:,2], c='blue', marker='X', s=100)
    plt.pause(0.01)
plt.show()
#sub.plotData(data, centerPoints)

#Step 8. Keksipisteiden tallennus kmeans.h tiedostoon        
sub.printCenterPoints("kmeans.h",centerPoints,numberOfCP)

