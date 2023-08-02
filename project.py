import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ControlPin = [31, 36, 22, 37]

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

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)
GPIO.setup(29, GPIO.IN)

while True:
    if (GPIO.input(15)==0):
        print("click")
        for i in range(0, 500):
            for fullstep in range(4):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[fullstep] [pin])
                    time.sleep(0.001)
                    GPIO.cleanup
        time.sleep(0.3)
    
    if (GPIO.input(29)==0):
        print("click 2")
        for i in range(0, 500):
            for fullstep in range(4):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], reverseseq[fullstep] [pin])
                    time.sleep(0.001)
                    GPIO.cleanup
        time.sleep(0.3)