import smbus
import time
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)
 
# This is the address we setup in the Arduino Program
address = 0x04
 
def writeData(value):
    #bus.write_byte(address,88)
    bus.write_byte(address, value)
    bus.write_i2c_block_data(address,v1,[v2,v3,v4])
    # bus.write_byte_data(address, 0, value)
    return -1
 
def writeNumber(v1, v2):
        bus.write_i2c_block_data(address,v1,[v2])
        return -1
 
#def readNumber():
    #number = bus.read_byte(address)
    ## number = bus.read_byte_data(address, 1)
    #return number
 
while True:
    axis = input("Axis 88 or 89: ")
    number = readNumber()
    parameter = input("parameter: ")
    
    if not parameter:
        continue
 
    #writeData(axis)
    #writeData(parameter)
    
    WriteNumber(axis, parameter)
    
    #print "RPI: Hi Arduino, I sent you ", axis, parameter
    # sleep one second
    #time.sleep(1)
 
    # number = readNumber()
    # print "Arduino: Hey RPI, I received a digit ", number
    print