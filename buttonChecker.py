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

    global buttonPressed
    buttonPressed = True
    self.running = True
    self.last_press = None

  def run(self):
    global buttonPressed
    try:
      while self.running:
        print "Waiting for signal"
        GPIO.wait_for_edge(self.buttonPin, GPIO.FALLING)
        print "Received signal"

        millis = int(round(time.time() * 1000))
        if self.last_press:
          if self.last_press - millis > 700:
            buttonPressed = not buttonPressed
        self.last_press = millis
        
        GPIO.wait_for_edge(self.buttonPin, GPIO.RISING)
        print "Button released"

    except KeyboardInterrupt:
      GPIO.cleanup()
    GPIO.cleanup()
