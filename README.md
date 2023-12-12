# Tietoliikenteen sovellusprojekti
Projektissa tehtävänä on suunnitella Nordic NRF5340 DK -alustalle ohjelma, joka mittaa kiihtyvyysanturidataa (GY-61) ja välittää tietoa langattomasti IoT-reitittimelle (Raspberry Pi). Raspberry välittää dataa Oamkin MySQL-palvelimelle.

Tietokantaan tallentuvaan dataan on TCP-sokettirajapinta ja yksinkertainen HTTP API. Kerättyä dataa haetaan HTTP-rajanpinnasta omaan kannettavaan koodatulla ohjelmalla ja käsitellään koneoppimistarkoituksiin.  

>Projektin vaiheet:
>
>1. Kiihtyvyysanturimittaukset, C & NRF5340DK
>2. Kiihtyvyysanturidatan siirto tietokantaan, C & Python
>3. TCP client datan lukemien tietokannasta, Python
>4. K-means opetusalgoritmi ja opetus, Python
>5. K-means mittaukset + confusion matrix, C & NRF5340DK

<br/>

<picture>
 <img alt="Arkkitehtuurikuva" src="arkkitehtuurikuva.png">
</picture>

*Kuva 1. Arkkitehtuurikuva projektista.*

## Kiihtyvyysanturimittaukset ja datansiirto tietokantaan

Mittaukset ja tallennus tietokantaan toteutettiin pitämällä anturia aina yhteen suuntaan kerrallaan ja samalla tälle suunnalle annettiin numero (label), joka toimii suuntatietona neuroverkolle. Annoimme vaihtelua sensoridatalle heiluttamalla anturia mittausta tehdessä.

#### Suunta ja label:  

x-akseli alas = 0  
x-akseli ylös = 1  
y-akseli alas = 2  
y-akseli ylös = 3  
z-akseli alas = 4  
z-akseli ylös = 5


## K-means opetusalgoritmi
K-means opetusalgoritmillä sensoridatasta saadaan tunnistettua ja luokiteltua kaikki kuusi eri suuntaa keskipisteiden avulla. 
- Opetus (luokittelu) aloitetaan arvaamalla ensin kuusi satunnaista keskipistettä ja laskemalla kaikkien tunnettujen pisteiden etäisyys, jokaiseen arvottuun keksipisteeseen.  
- Jokaiselle keskipisteelle on laskuri- ja kumulatiivinen summataulukko, johon tallennetaan voittajan eli lähinnä olevan pisteen koordinaatit. Laskuria kasvatetaan aina voittajan keksipisteen kohdalla.  
- Tämän jälkeen lasketaan uudet keskipisteet kumulatiivisen summa- ja laskuriarvojen avulla (keskiarvo). Jos jokin keskipiste ei saanut yhtään voittoa, niin sille arvotaan uusi satunnainen keskipiste.  
- Tätä toistetaan niin kauan että luokittelu onnistuu.
- Lopputuloksena saatiin keskipisteet.h tiedosto, joka sisältää kaikki kuusi opetettua keskipistettä.  

<picture>
 <img alt="Sensoridata3D" src="Sensoridata3D.png">
</picture>

*Kuva 2. Sensoridata 3D-avaruudessa, ennen luokittelua.*

<picture>
 <img alt="Arvotut keskipisteet" src="kmeans.png">
</picture>

*Kuva 3. Sensoridata ja arvotut keskipisteet.*

<picture>
 <img alt="K-means opetus" src="kmeans.gif">
</picture>

*Kuva 4. K-means-algoritmin opetus.* 

## Neuroverkon opetus

<picture>
 <img alt="Neuroverkon rakenne" src="neuroverkko.png">
</picture>

*Kuva 5. Neuroverkon rakenteen suunnitelma*

Neuroverkolle annetaan x,y ja z arvot sekä suuntatieto (luokka), jonka mukaan neuroverkko luokittelee x,y ja z arvot kuuteen eri luokkaan.

<picture>
 <img alt="Keras malli" src="keras.png">
</picture>

*Kuva 5. Mallin rakennus Colabissa*

Neuroverkko opetettiin ja testattiin Googlen Colabissa ja sieltä tuloksena saatiin säädettävät parametrit (eli painokertoimet ja biakset), csv-tiedostoina. Erillisellä python koodilla ja samoja parametreja käyttämällä, saimme saman neuroverkon tuloksen kuin Colabissa, model.predict-funktiolla. 

## Confusion matrix

K-means algoritmi ja neuroverkko toteutettiin NRF5340dk-alustalle, jossa molempia testattiin ottamalla 100kpl kiihtyvyysanturimittauksia, yhtä suuntaa kohden. Tuloksena tästä saatiin confusion matrix, jossa verrattiin todellisia luokkia, ennustettuihin luokkiin. Confusion matrix kertoo kuinka hyvin koneoppimismalli toimii, eli vastaako ennuste todellista arvoa.

<picture>
 <img alt="confusion" src="ConfusionMatrix.png">
</picture>

*Kuva 6. Confusion matrixit tulostettuna sarjamonitorille*

Molemmat koneoppimismallit onnistuivat luokittelussa erittäin hyvällä tarkkuudella. Vastaavaan tulokseen pääseminen olisi ollut haastava totetuttaa esim. päätöspuulla, ja olisi todennäköisesti antanut epätarkemmat tulokset, koska raja-arvojen määrittäminen manuaalisesti olisi hankalaa.