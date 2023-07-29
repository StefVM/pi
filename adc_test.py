import cgitb ; cgitb.enable()
import spidev
import time
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs0 = digitalio.DigitalInOut(board.CE0)
adc = SPIDevice(spi, cs0, baudrate= 1000000)

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    with adc:
        r = bytearray(3)
        spi.write_readinto([1, (8+adcnum)<<4, 0], r)
        time.sleep(0.000005)
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

while True:
    tmp = readadc(0)
    print("input: ", tmp)
    time.sleep(0.2)