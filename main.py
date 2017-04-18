#!/usr/bin/python
from lcd_module import LCDController
import smbus
import time
from data_fetch import getData, RCP_OK, RCP_FAIL
from data_write import DataWriter
import gpsdData
from gpsdData import GpsPoller
import math

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

  while running:

    running = updateRunSignal() #check if we need to shut down
    saving = updateSaveSignal() #check if we need to save
