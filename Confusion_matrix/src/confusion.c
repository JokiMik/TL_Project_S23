#include <zephyr/kernel.h>
#include <math.h>
#include "confusion.h"
#include "adc.h"
#include "keskipisteet.h"
#include "neuroverkonKertoimet.h"
#include <time.h>

/* 
  K-means algorithm should provide 6 center points with
  3 values x,y,z. Let's test measurement system with known
  center points. I.e. x,y,z are supposed to have only values
  1 = down and 2 = up
  
  CP matrix is thus the 6 center points got from K-means algoritm
  teaching process. This should actually come from include file like
  #include "KmeansCenterPoints.h"
  
  And measurements matrix is just fake matrix for testing purpose
  actual measurements are taken from ADC when accelerator is connected.
*/ 
#define DEBUG 0

int CP[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int measurements[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int CM[6][6]= {0};

int CM2[6][6]= {0};

//relu ja softmax funktiot
void relu(float *array, int size) 
{
    for (int i = 0; i < size; ++i) 
	{
        if (array[i] < 0) {
            array[i] = 0;
        }
    }
}
void softmax(float* x, int length) {
    float max = -__FLT_MAX__; //alustus pienimmällä float luvulla (=suurin negatiivinen luku)
    float sum = 0;

    // Etsitään suurin arvo
    for (int i = 0; i < length; i++) {
        if (x[i] > max) {
            max = x[i];
        }
    }

    // Vähennetään suurin arvo ja lasketaan e:n potenssiin x jokaiselle x:n alkiolle
    // Laske näiden summa
    for (int i = 0; i < length; i++) {
        x[i] = exp(x[i] - max);	//Vähennetään suurin arvo vektorista ennen e:n potenssiin laskemista (estää ylivuodon)
        sum = sum + x[i];
    }

    // Jaa jokainen alkio summan arvolla
    for (int i = 0; i < length; i++) {
        x[i] = x[i] / sum;
    }
}

void makeClassificationWithNeuralNetwork(int direction)
{
   struct Measurement m = readADCValue();
   float a0[3] = {m.x, m.y, m.z}; //input data
   //float a0[3] = {1200,1500,1500};
	float a1[10] = {0};	//hidden layer
	float a2[6] = {0}; //output layer
	int a0Rows = 3;
	int w1Cols = 10;
	int w2Cols = 6;

	//Lasketaan matmul a0 * W1
	for (int i = 0; i < w1Cols; ++i) 
	{
		for (int j = 0; j < a0Rows; ++j) 
		{
			a1[i] = a1[i] + a0[j] * W1[j][i];
		}
	}
   //Lasketaan a1 + b1
	for (int i = 0; i < w1Cols; ++i) 
	{
		a1[i] = a1[i] + B1[i];
	}
   //Lasketeaan relu(a1)
	relu(a1, w1Cols);

	for (int i = 0; i < w2Cols; ++i) 
	{
		for (int j = 0; j < w1Cols; ++j) 
		{
			a2[i] = a2[i] + a1[j] * W2[j][i];
		}
	}
	for (int i = 0; i < w2Cols; ++i) 
	{
		a2[i] = a2[i] + B2[i];
	}
   //Lasketaan a2 + b2
	for (int i = 0; i < w2Cols; ++i) 
	{
		a2[i] = a2[i] + B2[i];
	}
   //Lasketaan softmax(a2)
	softmax(a2, w2Cols);

   //Lasketaan voittaja eli se indeksi, jolla on suurin arvo
   int winnerIndex = 0;
   float max = -__FLT_MAX__; //alustus pienimmällä float luvulla (=suurin negatiivinen luku)
   for (int i = 0; i < w2Cols; i++) {
        if (a2[i] > max) { //Etsitään suurin arvo
            max = a2[i]; //Tallennetaan suurin arvo
            winnerIndex = i;
        }
    }
   printk("\nVoittaja = %d\n", winnerIndex + 1);
   CM2[direction][winnerIndex]++; //Kasvatetaan suunnan ja voittajan indeksin mukaista solua yhdellä
}

void printConfusionMatrix(void)
{
	printk("Confusion matrix (k-means) = \t");
   printk("Confusion matrix (neural network) = \n");
	printk("   cp1 cp2 cp3 cp4 cp5 cp6\t");
   printk("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printk("cp%d %d   %d   %d   %d   %d   %d\t",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
      printk("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM2[i][0],CM2[i][1],CM2[i][2],CM2[i][3],CM2[i][4],CM2[i][5]);
	}
}

void makeHundredFakeClassifications(void)
{
   /*******************************************
   Jos ja toivottavasti kun teet toteutuksen paloissa eli varmistat ensin,
   että etäisyyden laskenta 6 keskipisteeseen toimii ja osaat valita 6 etäisyydestä
   voittajaksi sen lyhyimmän etäisyyden, niin silloin voit käyttää tätä aliohjelmaa
   varmistaaksesi, että etäisuuden laskenta ja luokittelu toimii varmasti tunnetulla
   itse keksimälläsi sensoridatalla ja itse keksimilläsi keskipisteillä.
   *******************************************/
   for(int i = 0; i < 100; i++)
   {
      for(int j = 0; j < 6; j++)
      {
         int winnerIndex = calculateDistanceToAllCentrePointsAndSelectWinner(measurements[j][0], measurements[j][1], measurements[j][2]);
         CM[j][winnerIndex]++; //Kasvatetaan suunnan ja voittajan indeksin mukaista solua yhdellä
      }

   }
}

void makeOneClassificationAndUpdateConfusionMatrix(int direction)
{
   /**************************************
   Tee toteutus tälle ja voit tietysti muuttaa tämän aliohjelman sellaiseksi,
   että se tekee esim 100 kpl mittauksia tai sitten niin, että tätä funktiota
   kutsutaan 100 kertaa yhden mittauksen ja sen luokittelun tekemiseksi.
   **************************************/
   struct Measurement m = readADCValue();
   int winnerIndex = calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);
   CM[direction][winnerIndex]++; //Kasvatetaan suunnan ja voittajan indeksin mukaista solua yhdellä
   printk("Voittaja = %d\n", winnerIndex + 1);
}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
   /***************************************
   Tämän aliohjelma ottaa yhden kiihtyvyysanturin mittauksen x,y,z,
   laskee etäisyyden kaikkiin 6 K-means keskipisteisiin ja valitsee
   sen keskipisteen, jonka etäisyys mittaustulokseen on lyhyin.
   ***************************************/
   
   float distances[6] = {0}; //Taulukko etäisyyksien tallentamiseksi
   float minDistance = __FLT_MAX__;//Muuttuja lyhimmän etäisyyden tallentamiseksi, alustus suurimmalla float luvulla.
   int winnerIndex = 0; //Muuttuja voittajan tallentamiseksi
   
   float fx = (float)x; //Muutetaan intit floateiksi
   float fy = (float)y;
   float fz = (float)z;
   for(int i = 0; i < 6; i++)
   {
      #if DEBUG
      distances[i] = sqrt(pow(fx-CP[i][0],2) + pow(fy-CP[i][1],2) + pow(fz-CP[i][2],2));
      #else
      distances[i] = sqrt(pow(fx-centerPoints[i][0],2) + pow(fy-centerPoints[i][1],2) + pow(fz-centerPoints[i][2],2));
      #endif
      printk("Etäisyys keskipisteeseen %d = %f\n", i+1, distances[i]);

      if(distances[i] < minDistance) //Tarkistetaan onko etäisyys lyhyempi kuin aikaisempi lyhin etäisyys
      {
         minDistance = distances[i]; //Jos on niin tallennetaan uusi lyhin etäisyys
         winnerIndex = i; //Tallennetaan voittajan indeksi
      }
   }
   return winnerIndex;
}

void resetConfusionMatrix(int state)
{
	for(int i=0;i<6;i++)
	{ 
		for(int j = 0;j<6;j++)
		{
         if(state == 0)
         {
            CM[i][j]=0;
         }
         else
         {
            CM2[i][j]=0;
         }
		}
	}
}

