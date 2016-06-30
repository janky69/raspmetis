#!/usr/bin/python
from lcd_module import LCDController
import smbus
import time
from data_fetch import getData, RCP_OK, RCP_FAIL
from data_write import DataWriter

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25

LCDOK = 1
LCDFAIL = 0
GPSOK = 1
GPSFAIL = 0

def lcdplot(lcd_controller, data, ardu_status, gps_status):
  if ardu_status == RCP_OK:
    ardu_plot_status = "*"
  else:
    ardu_plot_status = "_"

  if gps_status == GPSOK:
    gps_plot_status = "*"
  else:
    gps_plot_status = "_"

  lcd_controller.plot(
    "Wind spd: %03d A%s" % (data[1],ardu_plot_status),
    "Wind dir: %03d G%s" % (data[0],gps_plot_status)
  )

if __name__ == "__main__":
  lcd_status = LCDFAIL
  ardu_status = RCP_FAIL
  lcd = LCDController()
  datawriter = DataWriter("/home/pi/testdata.csv")

  while True:
    try:
      # get data from arduino
      data = getData()
      ardu_status = data[3]

      # set up the lcd
      if lcd_status == LCDFAIL:
        lcd.initialize()
        lcd_status = LCDOK
      lcdplot(lcd, data, ardu_status, 0)
      #lcd.plot("Wind spd: %03d" % data[1],"Wind dir: %03d" % data[0])
      if ardu_status == RCP_OK:
        datawriter.append("%d,%d,%d"%(data[0],data[1],data[2]))
    except (KeyboardInterrupt, SystemExit):
      if lcd_status == LCDOK:
        lcd.plot("Quitting, bye!","")
      raise
    except:
      lcd_status = LCDFAIL

    try:
      time.sleep(.5)
    except (KeyboardInterrupt, SystemExit):
      if lcd_status == LCDOK:
        lcd.plot("Quitting, bye!","")
      raise
