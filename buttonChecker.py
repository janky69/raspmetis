#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv/
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

# GPIO 23 set up as input. It is pulled up to stop false signals

buttonPressed = None

class buttonController(threading.Thread):
  def __init__(self,buttonPin=23):
    threading.Thread.__init__(self)

    self.buttonPin = buttonPin
    GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    self.buttonPressed = False
    self.running = True
    self.last_press = int(round(time.time() * 1000))

  def run(self):
    try:
      while self.running:
        print "Waiting for signal"
        GPIO.wait_for_edge(self.buttonPin, GPIO.FALLING)
        print "Received signal"

        millis = int(round(time.time() * 1000))
        if millis - self.last_press > 700:
          self.buttonPressed = not self.buttonPressed
        self.last_press = millis
        print("Millis: %d, Button: %r" % (millis, self.buttonPressed))
        
        GPIO.wait_for_edge(self.buttonPin, GPIO.RISING)
        print "Button released"

    except KeyboardInterrupt:
      GPIO.cleanup()
    GPIO.cleanup()
