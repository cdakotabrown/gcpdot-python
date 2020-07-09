#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import laurel
import time
import os

USERNAME=os.environ.get('BULB_USER')
PASSWORD=os.environ.get('BULB_PASS')

def get_dot_color():
        URL = "http://global-mind.org/gcpdot/gcpindex.php?current=1?nonce=10000"
        DOT_COLORS = [
        (0.01,   [0xff,0xa8,0xc0]),
        (0.0,    [0xff,0x1e,0x1e]),
        (0.08,   [0xff,0xb8,0x2e]),
        (0.15,   [0xff,0xd5,0x17]),
        (0.23,   [0xff,0xfa,0x40]),
        (0.3,    [0xf9,0xfa,0x00]),
        (0.4,    [0xae,0xfa,0x00]),
        (0.9,    [0x64,0xfa,0x64]),
        (0.9125, [0x64,0xfa,0xab]),
        (0.93,   [0xac,0xf2,0xff]),
        (0.96,   [0x0e,0xee,0xff]),
        (0.98,   [0x24,0xcb,0xfd]),
        (1.0,    [0x56,0x55,0xca])]
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")
        index = float(soup.find('s').contents[0])
        print(index)
        return next((color[1] for color in DOT_COLORS if color[0] >= index), None)

def init_bulb():
    devices = laurel.laurel(USERNAME, PASSWORD)
    primary = devices.devices[0]
    mesh_network = devices.networks[0]
    mesh_network.connect()
    return primary
    
print("Bulb control running")

bulb = init_bulb()
bulb.set_temperature(1)
print(bulb.name)
print(bulb.id)
print(bulb.type)
print(bulb.brightness)
print(bulb.temperature)

while (True):
    c = get_dot_color()
    bulb.set_rgb(c[0], c[1], c[2])
    bulb.set_brightness(1)
    time.sleep(60)

