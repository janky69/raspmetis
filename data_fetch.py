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

while True:
#	var = input("Enter 1 - 9: ")
#	if not var:
#		continue
#	writeNumber(var)
#	print "RPI: Hi Arduino, I sent you", var
	# sleep one second
	time.sleep(1)
	
	numbers = readNumber()
#	print "Arduino: Hey RPI, I received a digit ", number
	print numbers
