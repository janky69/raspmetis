from lcd_module import LCDController
import smbus
import time

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25


if __name__ == "__main__":
  lcd = LCDController()
  
  while True:
    # get data from arduino

    try:
      lcd.plot("Yo, come va?","Ohhhh")
    except:
      pass
    time.sleep(.5)
