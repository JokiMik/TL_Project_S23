import numpy as np
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    #Step 3. Testataan etäisyys laskuria
    piste1 = np.array([1,1,1])
    piste2 = np.array([2,2,2])
    etaisyys = etaisyysLaskuri(piste1,piste2)
    print("Etäisyys testilasku (neliöjuuri 3) = ",etaisyys)
