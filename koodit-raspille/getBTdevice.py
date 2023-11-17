'''
Esimerkkikoodipohjat: https://pypi.org/project/bleak/
pip install bleak
'''

#Etsii bluetooth laitteet ja tulostaa ne
import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

asyncio.run(main())