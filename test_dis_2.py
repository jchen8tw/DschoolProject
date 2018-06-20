import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
GPIO.output(GPIO_TRIGGER, False)
time.sleep(0.5)
GPIO.output(GPIO_TRIGGER, True)
time.sleep(0.00001)
GPIO.output(GPIO_TRIGGER, False)
stop = time.time()
start = time.time()
if GPIO.input(GPIO_ECHO)==0:
    start = time.time()
if GPIO.input(GPIO_ECHO)==1:
    stop = time.time()
elapsed = stop-start

# Distance pulse travelled in that time is time
# multiplied by the speed of sound (cm/s)
distance = elapsed * 34000

# That was the distance there and back so halve the value
distance = distance / 2
a=105
while a<100:
    print "Distance : %.1f" % distance
    a=a-1
    print a
# Reset GPIO settings
    GPIO.cleanup()
