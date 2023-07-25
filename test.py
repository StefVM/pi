#!/usr/bin/env python3
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

dc = digitalio.DigitalInOut(board.D23)
csl = digitalio.DigitalInOut(board.CE1)
reset = digitalio.DigitalInOut(board.D24)
display = adafruit_pcd8544.PCD8544(spi, dc, csl, reset, baudrate=1000000)
display.bias = 4
display.contrast = 60
display.invert = True

display.fill(0)
display.show()

font = ImageFont.load_default()

image = Image.new('1', (display.width, display.height))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

draw.text((1,0), 'Test1', font=font)
draw.text((1,8), 'Test2', font=font)
draw.text((1,16), 'Test3', font=font)
draw.text((1,24), 'Test4', font=font)
draw.text((1,32), 'Test5', font=font)
display.image(image)
display.show()