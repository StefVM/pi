import RPi.GPIO as GPIO
import time
GPIO.cleanup

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)
GPIO.setup(29, GPIO.IN)

while True:
    if (GPIO.input(15)==0):
        print("click")
        time.sleep(0.3)
    
    if (GPIO.input(29)==0):
        print("click 2")
        time.sleep(0.3)