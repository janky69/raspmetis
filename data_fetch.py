import smbus
import time

bus = smbus.SMBus(1) # User SMBus(0) for version 1

# The address we setup in the Arduino Program
address = 0x25

def writeNumber(value):
  bus.write_byte(address, value)
# bus.write_byte_data(address, 0, value)
  return -1

def readNumber():
#number = bus.read_byte(address)
#number = bus.read_byte_data(address, 4)
  numbers = bus.read_i2c_block_data(address, 4)
  return numbers


#while True:
#	var = input("Enter 1 - 9: ")
#	if not var:
#		continue
#	writeNumber(var)
#	print "RPI: Hi Arduino, I sent you", var
# sleep one second
#  time.sleep(1)

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

#	print "Arduino: Hey RPI, I received a digit ", number
#  print "%d -> %d -> %d" %(wind_direction_c, wind_direction_p, wind_direction)
#  print "Wind speed: %d" %(wind_speed)
