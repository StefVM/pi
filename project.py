import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import cgitb ; cgitb.enable()
import spidev
from adafruit_bus_device.spi_device import SPIDevice

GPIO.cleanup

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs0 = digitalio.DigitalInOut(board.CE0)
adc = SPIDevice(spi, cs0, baudrate= 1000000)
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

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    with adc:
        r = bytearray(3)
        spi.write_readinto([1, (8+adcnum)<<4, 0], r)
        time.sleep(0.000005)
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

PIN_TRIGGER = 11
PIN_ECHO = 13

ControlPin = [18, 22, 24, 26]

for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

reverseseq = [[1, 0, 0, 1],
       [0, 0, 1, 1],
       [0, 1, 1, 0],
       [1, 1, 0, 0]]

seq = [[1, 1, 0, 0],
       [0, 1, 1, 0],
       [0, 0, 1, 1],
       [1, 0, 0, 1]]

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)

print ("Waiting for sensor to settle")

time.sleep(2)

print("Calculating distance")

GPIO.setup(15, GPIO.IN)
GPIO.setup(29, GPIO.IN)

status = "armed"

triggercount = 0

while True:
    tmp = readadc(0)
    print("input: ", tmp)
    time.sleep(0.2)

    if (GPIO.input(15)==0):
        for i in range(0, 500):
            for fullstep in range(4):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[fullstep] [pin])
                    time.sleep(0.001)
        status = "triggered"
        triggercount =+ 1 
        time.sleep(0.3)
    
    if (GPIO.input(29)==0):
        status = "off"
        for i in range(0, 500):
            for fullstep in range(4):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], reverseseq[fullstep] [pin])
                    time.sleep(0.001)
        time.sleep(30)
        status = "armed"
    
    
    
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
        pulse_start_time = time.time()
      
    while GPIO.input(PIN_ECHO)==1:
        pulse_end_time = time.time()        
      

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17000, 2)
    print("Distance:",distance,"cm")

    trigger_distance = tmp / 100
    if distance <= trigger_distance:
        for i in range(0, 500):
            for fullstep in range(4):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[fullstep] [pin])
                    time.sleep(0.001)
        status = "triggered"
        triggercount =+ 1 
        time.sleep(0.3)

    time.sleep(3)

    draw.text((1,0), 'Distance: ', distance, font=font)
    draw.text((1,0), 'Trigger distance: ', trigger_distance, font=font)
    draw.text((1,0), 'Status:  ', status, font=font)
    draw.text((1,0), 'Triggers:  ', triggercount, font=font)