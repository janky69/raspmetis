#!/usr/bin/python
from lcd_module import LCDController
import smbus
import time
from data_fetch import getData, RCP_OK, RCP_FAIL
from data_write import DataWriter
import gpsdData
from gpsdData import GpsPoller
import math
import buttonChecker
from buttonChecker import buttonController

from utils import *

def updateSaveSignal():
  return False

def updateRunSignal():
  return True

if __name__ == '__main__':
  running = True
  saving = False

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
  buttonc = buttonController()
  buttonc.start()

  while running:

    running = updateRunSignal() #check if we need to shut down
    saving = buttonChecker.buttonPressed #check if we need to save

    try:

      # get data from arduino
      data = getData()
      ardu_status = 1 if saving else 0 # debug value

      # Start the gps watcher
      try:
        if not gpsp.running:
          gpsp.running = True
          gpsp.start()
          gps_status = GPSOK
      except:
        gpsp.running = False
        gps_status = GPSFAIL
        raise

      try:
        adj_speed = compute_wind_speed(data[1],data[0],gpsd.speed)
        data[1] = adj_speed
      except:
        pass

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
      if ardu_status == RCP_OK and saving:
        datawriter.append("%d,%d,%d"%(data[0],data[1],data[2]))

      # Wait before next rount
      time.sleep(.5)

    except (KeyboardInterrupt, SystemExit):
      if lcd_status == LCDOK:
        lcd.plot("Quitting, bye!","")
      gpsp.running = False
      gpsp.join()
      raise

    except:
      raise
