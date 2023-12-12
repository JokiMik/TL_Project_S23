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

## Kiihtyvyysanturimittaukset ja datan siirto tietokantaan

Mittaukset ja tallennus tietokantaan toteutettiin pitämällä anturia aina yhteen suuntaan kerrallaan ja samalla tälle suunnalle annettiin numero (label), joka toimii suuntatietona neuroverkolle.

#### Suunta ja label:  

x-akseli alas = 0  
x-akseli ylös = 1  
y-akseli alas = 2  
y-akseli ylös = 3  
z-akseli alas = 4  
z-akseli ylös = 5


## K-means opetusalgoritmi
K-means opetusalgoritmillä sensoridatasta saadaan tunnistettua ja luokiteltua kaikki kuusi eri suuntaa keskipisteiden avulla. Kuusi suuntaa ovat siis x,y ja z, joista jokainen sekä ylös että alas.  
- Opetus (luokittelu) aloitetaan arvaamalla ensin kuusi satunnaista keskipistettä ja laskemalla kaikkien tunnettujen pisteiden etäisyys, jokaiseen arvottuun keksipisteeseen.  
- Jokaiselle keskipisteelle on laskuri- ja kumulatiivinen summa -taulukko, johon tallennetaan voittajan eli lähinnä olevan pisteen koordinaatit. Laskuria kasvatetaan aina voittajan keksipisteen kohdalla.  
- Tämän jälkeen lasketaan uudet keskipisteet kumulatiivisen summa- ja laskurin arvojen avulla (keskiarvo). Jos jokin keskipiste ei saanut yhtään voittoa, niin sille arvotaan uusi satunnainen keskipiste.  
- Tätä toistetaan niin kauan että luokittelu onnistuu.  

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

