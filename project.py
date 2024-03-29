import RPi.GPIO as GPIO
import time
import cgitb; cgitb.enable()
import spidev
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import requests

try:
    ControlPin = [6, 16, 25, 26]

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    cs0 = digitalio.DigitalInOut(board.CE0)
    adc = SPIDevice(spi, cs0, baudrate=1000000)
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


    def readadc(adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        with adc:
            r = bytearray(3)
            spi.write_readinto([1, (8 + adcnum) << 4, 0], r)
            time.sleep(0.000005)
            adcout = ((r[1] & 3) << 8) + r[2]
            return adcout


    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seq = [[1, 0, 0, 1],
           [0, 0, 1, 1],
           [0, 1, 1, 0],
           [1, 1, 0, 0]]

    reverseseq = [[1, 1, 0, 0],
                  [0, 1, 1, 0],
                  [0, 0, 1, 1],
                  [1, 0, 0, 1]]

    status = "on"
    statusvalue = 2
    triggercount = 0

    url = "http://stefvm.hub.ubeac.io/iotessStefVM"
    uid = "iotessStefVM"

    GPIO.setup(22, GPIO.IN)
    GPIO.setup(5, GPIO.IN)

    PIN_TRIGGER = 17
    PIN_ECHO = 27

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    time.sleep(2)

    while True:
        tmp = readadc(0)
        time.sleep(0.2)
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()

        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17000, 2)
        trigger_distance = round(5 + tmp / 50, 2)
        if status == "on":
            if (distance < trigger_distance):
                for i in range(0, 100):
                    for fullstep in range(4):
                        for pin in range(4):
                            GPIO.output(ControlPin[pin], seq[fullstep][pin])
                            time.sleep(0.0005)
                            GPIO.cleanup
                triggercount += 1
                status = "triggered"
                statusvalue = 1

        if status == "on":
            if (GPIO.input(22) == 0):
                for i in range(0, 100):
                    for fullstep in range(4):
                        for pin in range(4):
                            GPIO.output(ControlPin[pin], seq[fullstep][pin])
                            time.sleep(0.0005)
                            GPIO.cleanup
                triggercount += 1
                status = "triggered"
                statusvalue = 1
                time.sleep(0.3)

        if status == "triggered":
            if (GPIO.input(5) == 0):
                for i in range(0, 100):
                    for fullstep in range(4):
                        for pin in range(4):
                            GPIO.output(ControlPin[pin], reverseseq[fullstep][pin])
                            time.sleep(0.0005)
                            GPIO.cleanup
                status = "off"
                statusvalue = 0
                draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
                draw.text((1, 0), 'Dist: ' + str(distance) + "cm", font=font)
                draw.text((1, 8), 'Trig: ' + str(trigger_distance) + "cm", font=font)
                draw.text((1, 16), 'Status: ' + status, font=font)
                draw.text((1, 24), 'Triggers: ' + str(triggercount), font=font)
                display.image(image)
                display.show()
                data = {
                    "id": uid,
                    "sensors": [{
                        'id': 'status',
                        'data': statusvalue
                    },
                        {
                            'id': 'triggers',
                            'data': triggercount
                        }]
                }
                r = requests.post(url, verify=False, json=data)
                time.sleep(20)
                status = "on"
                statusvalue = 2
                time.sleep(0.3)

        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
        draw.text((1, 0), 'Dist: ' + str(distance) + "cm", font=font)
        draw.text((1, 8), 'Trig: ' + str(trigger_distance) + "cm", font=font)
        draw.text((1, 16), 'Status: ' + status, font=font)
        draw.text((1, 24), 'Triggers: ' + str(triggercount), font=font)
        display.image(image)
        display.show()

        data = {
            "id": uid,
            "sensors": [{
                'id': 'status',
                'data': statusvalue
            },
                {
                    'id': 'triggers',
                    'data': triggercount
                }]
        }

        r = requests.post(url, verify=False, json=data)

        time.sleep(2)

finally:
    GPIO.cleanup()