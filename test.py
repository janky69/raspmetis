from lcd_module import LCDController
import smbus
import time
from data_fetch import getData

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25


if __name__ == "__main__":
  status = 0
  lcd = LCDController()
  
  while True:
    # get data from arduino
    data = getData()

    try:
      if status == 0:
        lcd.initialize()
        status = 1
      lcd.plot("Wind speed: %d" % data[1],"Wind direction: %d" % data[0])
    except:
      status = 0
    time.sleep(.5)
