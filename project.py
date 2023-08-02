import RPi.GPIO as GPIO
import time

try:
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

    PIN_TRIGGER = 11
    PIN_ECHO = 13

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print ("Waiting for sensor to settle")

    time.sleep(2)

    print("Calculating distance")

    while True:
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
        trigger_distance = 5
        if (distance < trigger_distance):
            for i in range(0, 500):
                for fullstep in range(4):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin], seq[fullstep] [pin])
                        time.sleep(0.001)
                        GPIO.cleanup
        
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
        
        time.sleep(2)
    
finally:
    GPIO.cleanup()