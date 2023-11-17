'''
Esimerkkikoodipohjat: https://pypi.org/project/bleak/
pip install bleak
'''
#Ohjelma lukee sensoridataa bluetoothin kautta ja lähettää sen aliohjelman kautta tietokantaan

import asyncio
from bleak import BleakClient
import aliohjelma as db

address = "E5:3B:1D:2F:E7:BE" #nRF5340 laudan MAC-osoite
MODEL_NBR_UUID = "00001526-1212-efde-1523-785feabcd123" #MySensor characteristic UUID

counter = 0
pos_value = 0
x_value = 0
y_value = 0
z_value = 0

async def notification_handler(sender: str, data: bytearray):
    global counter, pos_value, x_value, y_value, z_value
    int_data = int.from_bytes(data, 'little')
    #print("Sensor data: ",int_data)
    '''
    Tiedetään että data tulee järjestyksessä suunta, x, y, z
    Tiedetään myös että suunta arvo on aina pienempi kuin 10
    Kasvatetaan laskuria aina kun saadaan uusi data, jonka avulla tiedetään missä kohtaa dataa ollaan.
    '''
    if int_data < 10:   #jos data on pienempi kuin 10, niin se on suunta
        pos_value = int_data
        print("Suunta: ", pos_value)
        counter = counter + 1 #kasvatetaan counteria, sen merkiksi että ollaan saatu suunta
    elif counter == 1:  #jos counter on 1 niin tiedetään että seuraava data on x
        x_value = int_data
        print("X: ", x_value)
        counter = counter + 1
    elif counter == 2:  
        y_value = int_data
        print("Y: ", y_value)
        counter = counter + 1
    elif counter == 3:
        z_value = int_data
        print("Z: ", z_value)
        counter = 0
        db.sendDataToDB(pos_value, x_value, y_value, z_value) #lähetetään data tietokantaan

async def main(address):
    async with BleakClient(address) as client:

        await client.start_notify(MODEL_NBR_UUID, notification_handler)
        await asyncio.sleep(3.0)  # aika kauanko luetaan dataa
        await client.stop_notify(MODEL_NBR_UUID)

asyncio.run(main(address))
