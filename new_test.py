import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ControlPin = [31, 36, 22, 37]

for pin in ControlPin:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

seq = [[1, 0, 0, 1],
       [0, 0, 1, 1],
       [0, 1, 1, 0],
       [1, 1, 0, 0]]

for i in range(0, 500):
    for fullstep in range(4):
        for pin in range(4):
            GPIO.output(ControlPin[pin], seq[fullstep] [pin])
            time.sleep(0.001)

#def blink(pin):
#    GPIO.setup(pin, GPIO.OUT)
#    GPIO.output(pin, 1)
#    time.sleep(0.5)
#    GPIO.output(pin, 0)
#    time.sleep(0.5)

#for i in range(0, 10):
#    blink(7)

GPIO.cleanup()
print("done")