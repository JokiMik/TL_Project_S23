import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

#Aliohjelma joka lähettää sensoridataa tietokantaan

def sendDataToDB(pos_value, x_value, y_value, z_value):
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_database = os.getenv("DB_DATABASE")

    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )
    mycursor = mydb.cursor()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    groupid = 5
    from_mac = "nrf5340"
    to_mac = "raspi"
    sensorvalue_f = "MI/MA"

    sql = "INSERT INTO rawdata (timestamp, groupid, from_mac, to_mac, sensorvalue_a, sensorvalue_b, sensorvalue_c, sensorvalue_d, sensorvalue_f) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (time,groupid,from_mac,to_mac,pos_value,x_value,y_value,z_value,sensorvalue_f)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "riviä lisätty tietokantaan.")
    mycursor.close()
    mydb.close()

if __name__ == "__main__":
    #sendDataToDB(1,2,3,4) #debug
    print("Tämä on aliohjelma, älä suorita tätä suoraan.")

