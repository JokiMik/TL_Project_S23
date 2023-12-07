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



void printConfusionMatrix(void)
{
	printk("Confusion matrix = \n");
	printk("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printk("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
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

void resetConfusionMatrix(void)
{
	for(int i=0;i<6;i++)
	{ 
		for(int j = 0;j<6;j++)
		{
			CM[i][j]=0;
		}
	}
}

