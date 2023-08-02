import RPi.GPIO as GPIO
import time
import cgitb ; cgitb.enable()
import spidev
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice

try:
    ControlPin = [6, 16, 15, 26]

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

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    seq = [[1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1]]

    reverseseq = [[1, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        [1, 1, 0, 0]]

    GPIO.setup(22, GPIO.IN)
    GPIO.setup(5, GPIO.IN)

    PIN_TRIGGER = 17
    PIN_ECHO = 27

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print ("Waiting for sensor to settle")

    time.sleep(2)

    print("Calculating distance")

    while True:
        tmp = readadc(0)
        print("input: ", tmp)
        time.sleep(0.2)
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
        trigger_distance = 2 + tmp/100
        print("Trigger distance:",trigger_distance,"cm")
        if (distance < trigger_distance):
            for i in range(0, 500):
                for fullstep in range(4):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin], seq[fullstep] [pin])
                        time.sleep(0.001)
                        GPIO.cleanup
        
        if (GPIO.input(22)==0):
            print("click")
            for i in range(0, 500):
                for fullstep in range(4):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin], seq[fullstep] [pin])
                        time.sleep(0.001)
                        GPIO.cleanup
            time.sleep(0.3)
        
        if (GPIO.input(5)==0):
            print("click 2")
            for i in range(0, 500):
                for fullstep in range(4):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin], reverseseq[fullstep] [pin])
                        time.sleep(0.001)
                        GPIO.cleanup
            time.sleep(0.3)
        
        time.sleep(2)
    
finally:
    GPIO.cleanup()