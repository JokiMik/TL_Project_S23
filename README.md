# Tietoliikenteen sovellusprojekti
Projektissa tehtävänä on suunnitella Nordic NRF5340 DK -alustalle client, joka mittaa kiihtyvyysanturidataa (GY-61) ja välittää tietoa langattomasti IoT-reitittimelle (Raspberry Pi). Raspberry välittää dataa Oamkin MySQL-palvelimelle.

Tietokantaan tallentuvaan dataan on TCP-sokettirajapinta ja yksinkertainen HTTP API. Kerättyä dataa haetaan HTTP-rajanpinnasta omaan kannettavaan koodatulla ohjelmalla ja käsitellään koneoppimistarkoituksiin.

<picture>
 <img alt="Arkkitehtuurikuva" src="arkkitehtuurikuva.png">
</picture>

1. Kiihtyvyysanturimittaukset, C & NRF5340DK
2. Kiihtyvyysanturidatan siirto tietokantaan, C & Python
3. TCP client datan lukemien tietokannasta, Python
2. K-means opetusalgoritmi ja opetus, Python
3. K-means mittaukset + confusion matrix, C & NRF5340DK