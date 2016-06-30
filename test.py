#!/usr/bin/python
from lcd_module import LCDController
import smbus
import time
from data_fetch import getData

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25

LCDOK = 1
LCDFAIL = 0

if __name__ == "__main__":
  lcd_status = LCDFAIL
  lcd = LCDController()
  
  while True:
    try:
      # get data from arduino
      data = getData()

      # set up the lcd
      if lcd_status == LCDFAIL:
        lcd.initialize()
        lcd_status = LCDOK
      lcd.plot("Wind speed: %d" % data[1],"Wind dir: %d" % data[0])
    except (KeyboardInterrupt, SystemExit):
      if lcd_status == LCDOK:
        lcd.plot("Quitting, bye!","")
      raise
    except:
      status = 0
    
    try:
      time.sleep(.5)
    except (KeyboardInterrupt, SystemExit):
      if lcd_status == LCDOK:
        lcd.plot("Quitting, bye!","")
      raise
