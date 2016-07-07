# Based on the code posted by Oscar Liang in https://oscarliang.com/raspberry-pi-arduino-connected-i2c/

import smbus
import time
import threading

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25

def writeNumber(value):
  bus.write_byte(address, value)
  return -1

def readNumber():
  numbers = bus.read_i2c_block_data(address, 4)
  return numbers


RCP_OK = 1
RCP_FAIL = 0

def getData():
  try:
    numbers = readNumber()
    numbers = numbers[:4]
  except:
    return 0,0,0,RCP_FAIL

  wind_direction_c = numbers[0] + (numbers[1] << 8)
  wind_speed = numbers[2]
  bat = numbers[3]
  wind_direction_p = int(wind_direction_c / 1023. * 360.)
  wind_direction = wind_direction_p
  if wind_direction > 180:
    wind_direction -= 360
  return wind_direction, wind_speed, bat, RCP_OK

def getAsyncData(recipient):
  try:
    numbers = readNumber()
    numbers = numbers[:4]
  except:
    recipient[0] = [ 0,0,0,RCP_FAIL ]

  wind_direction_c = numbers[0] + (numbers[1] << 8)
  wind_speed = numbers[2]
  bat = numbers[3]
  wind_direction_p = int(wind_direction_c / 1023. * 360.)
  wind_direction = wind_direction_p
  if wind_direction > 180:
    wind_direction -= 360
  recipient[0] = [ wind_direction, wind_speed, bat, RCP_OK ]
