import numpy as np
import matplotlib.pyplot as plt
import requests

#Hakee dataa kannasta grouopid:llä ja tallentaa sen csv tiedostoon
def getSensorData(groupid):
    url = f"http://172.20.241.9/luedataa_kannasta_groupid_csv.php?groupid={groupid}"  
    response = requests.get(url)
    #print(response.text)
    with open(f'group{groupid}_data.csv', 'w') as file:
        file.write(response.text)

# Tulostaa tunnetut ja arvotut pisteet 3D kuvaajaan
def plotData(data, centerPoints):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_title('Sensoridata 3D-avaruudessa')
    ax.set_xlabel('x-akseli')
    ax.set_ylabel('y-akseli')
    ax.set_zlabel('z-akseli')
    ax.scatter(data[:,0], data[:,1], data[:,2],c='red')
    ax.scatter(centerPoints[:,0], centerPoints[:,1], centerPoints[:,2],c='blue',marker='X', s=100)
    plt.show()

#Laskee etäisyydet keskipisteistä pisteisiin
def etaisyysLaskuri(p1, p2):
    etaisyys = np.sqrt(np.power(p2[0]-p1[0],2)  + np.power(p2[1]-p1[1],2)  +  np.power(p2[2]-p1[2],2))
    return(etaisyys)

#Tallennetaan keskipisteet kmeans.h tiedostoon
def printCenterPoints(filename,CP,numOfCP):
    #Järjestetään ensin keskipisteet haluttuun järjestykseen (ensimmäiseksi rivi jossa pienin x, sitten suurin x, pienin y, suurin y, pienin z, suurin z)
    # Etsitään rivit, joissa x, y ja z ovat pienimmillään ja suurimmillaan
    xmin = np.argmin(CP[:, 0])
    xmax = np.argmax(CP[:, 0])
    ymin = np.argmin(CP[:, 1])
    ymax = np.argmax(CP[:, 1])
    zmin = np.argmin(CP[:, 2])
    zmax = np.argmax(CP[:, 2])

    # Järjestetään keskipisteet haluttuun järjestykseen
    orderedIndices = [xmin, xmax, ymin, ymax, zmin, zmax]
    centerPoints = centerPoints[orderedIndices]

    with open (filename, 'w') as f:
        f.write("#ifndef KMEANS_H\n")
        f.write("#define KMEANS_H\n")
        f.write("const int centerPoints[6][3] = {\n")
        for i in range(numOfCP):
            f.write("{")
            f.write(str(CP[i,0])) #x
            f.write(",")
            f.write(str(CP[i,1])) #y
            f.write(",")
            f.write(str(CP[i,2])) #z
            f.write("},\n")
        f.write("};")
        f.write("\n#endif")
        f.close()
    print("Keskipisteet tallennettu kmeans.h tiedostoon")



if __name__ == "__main__":
    #Step 3. Testataan etäisyys laskuria
    piste1 = np.array([1,1,1])
    piste2 = np.array([2,2,2])
    etaisyys = etaisyysLaskuri(piste1,piste2)
    print("Etäisyys testilasku (neliöjuuri 3) = ",etaisyys)
    getSensorData(5)

