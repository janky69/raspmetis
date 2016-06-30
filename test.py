#!/usr/bin/python
from lcd_module import LCDController
import smbus
import time
from data_fetch import getData, RCP_OK, RCP_FAIL
from data_write import DataWriter
import gpsdData
from gpsdData import GpsPoller

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
  # Setup initial statuses
  gps_status = GPSFAIL
  lcd_status = LCDFAIL
  ardu_status = RCP_FAIL

  # Initialize controllers
  lcd = LCDController()
  datawriter = DataWriter(filename="/home/pi/testdata.csv")
  gpsp = GpsPoller()
  gpsd = gpsdData.gpsd
  gpsp.running = False
  # Check how these fail in case the gps module is not connected
  # see https://gist.github.com/wolfg1969/4653340 
  # and https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/using-your-gps
  # for examples

  while True:
    try:
      # get data from arduino
      data = getData()
      ardu_status = data[3]
      
      # Start the gps watcher
      try:
        if not gpsp.running:
          gpsp.start()
          gpsp.running = True
          gps_status = GPSOK
      except:
        gpsp.running = False
        gps_status = GPSFAIL
        raise

      # set up the lcd
      try:
        if lcd_status == LCDFAIL:
          lcd.initialize()
          lcd_status = LCDOK
        lcdplot(lcd, data, ardu_status, gps_status)
        #lcd.plot("Wind spd: %03d" % data[1],"Wind dir: %03d" % data[0])

      except IOError:
        lcd_status = LCDFAIL
      
      # Pass the data (formatted) to the datawriter
      if ardu_status == RCP_OK:
        datawriter.append("%d,%d,%d"%(data[0],data[1],data[2]))
      
      time.sleep(.5)

    except (KeyboardInterrupt, SystemExit):
      if lcd_status == LCDOK:
        lcd.plot("Quitting, bye!","")
      raise

    except:
      raise

