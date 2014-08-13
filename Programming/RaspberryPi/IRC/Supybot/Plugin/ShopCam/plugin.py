###
# Copyright (c) 2014, Technicus
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import smbus
import time

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('ShopCam')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class ShopCam(callbacks.Plugin):
    """Add the help for "@plugin help ShopCam". A plugin that sends stuff to an arduino"""
    # threaded = True 
    pass

    # for RPI version 1, use "bus = smbus.SMBus(0)"
    bus = smbus.SMBus(1)
    # This is the address we setup in the Arduino Program
    address = 0x04
    
    positionX = 0
    positionY = 90
    positionXCenter = 63
    positionYCenter = 191
    maxX = 90
    minX = -90
    maxY = 90
    minY = 0
    maxI2CX = 127
    minI2CX = 1
    maxI2CY = 128
    minI2CY = 255
    incrumentY = (90 / 4)
    incrumentX = (180 / 8)
    
    def mapRangeX(self, X0):
        if X0 < self.minX:
           X0 = self.minX
        if X0 > self.maxX:
           X0 = self.maxX
        #a1 = minX 
        #a2 = maxX
        #b1 = minI2CX
        #b2 = maxI2CX
        X1 = self.minI2CX + ((X0 - self.minX) * (self.maxI2CX - self.minI2CX) / (self.maxX - self.minX))
        return X1
     
    def mapRangeY(self, Y0):
        if Y0 < self.minY:
           Y0 = self.minY
        if Y0 > self.maxY:
           Y0 = self.maxY
        #a1 = minY 
        #a2 = maxY
        #b1 = minI2CY
        #b2 = maxI2CY
        Y1 = self.minI2CY + ((Y0 - self.minY) * (self.maxI2CY - self.minI2CY) / (self.maxY - self.minY))
        return Y1

    def writeNumber(self, value):
        self.bus.write_byte(self.address, value)
        # bus.write_byte_data(address, 0, value)
        return -1

    def readNumber(self):
        # number = 0
        self.bus.write_byte(self.address, number)
        # number = bus.read_byte_data(address, 1)
        return number

    #def move(self, irc, msg, args, var):
        #"""<byte>
        #Sends a byte (an integer from 1 to 255) to the arduino."""
        ## number = 0
        #if var < 128:
            #pan = var
        #else:
            #tilt = var
        #self.writeNumber(var)
        #time.sleep(1)
        #number = self.readNumber()
        #irc.reply('You moved the camera %d' % var)
        ##irc.reply('The Arduino answered: %d' % number)
    #move = wrap(move, ['int'])
    
    def move(self, irc, msg, args, X0, Y0):
        """< pan > < tilt >
        HeckBot expects integers from -90 to 90."""
        X1 = self.mapRangeX(X0)
        Y1 = self.mapRangeY(Y0)
        irc.reply('The result for X = ( %d )' %X1)
        irc.reply('The result for Y = ( %d )' %Y1)
        self.writeNumber(X1)
        #time.sleep(1)
        self.writeNumber(Y1)
        #time.sleep(1)
        irc.reply('You moved the camera to ( %d %d )' %(X1, Y1))
        self.positionX = X0
        self.positionY = Y0
    move = wrap(move, ['int','int'])

    def pan(self, irc, msg, args, X0):
        """< pan >
        HeckBot expects integers from -90 to 90."""
        X1 = self.mapRangeX(X0)
        irc.reply('The result for X = ( %d )' %X1)
        self.writeNumber(X1)
        irc.reply('You panned the camera to ( %d )' %X1)
        self.positionX = X0
    pan = wrap(pan, ['int'])
    
    def tilt(self, irc, msg, args, Y0):
        """< pan >
        HeckBot expects integers from -90 to 90."""
        Y1 = self.mapRangeY(Y0)
        irc.reply('The result for Y = ( %d )' %Y1)
        self.writeNumber(Y1)
        irc.reply('You tilted the camera to ( %d )' %Y1)
        self.positionY = Y0
    tilt = wrap(tilt, ['int'])

    def down(self, irc, msg, args, var):
        """< steps >
        HeckBot expects integers."""
        if (self.positionY <= (self.maxY - self.incrumentY)):
           self.positionY = self.positionY + self.incrumentY
           if self.positionY > self.maxY:
              self.positionY = self.maxY
           self.writeNumber(self.mapRangeY(self.positionY))
           irc.reply('You tilted the camera up to ( %d )' %self.positionY)
        elif ((self.positionY >= (self.maxY - self.incrumentY)) and (self.positionY < self.maxY)):
           if self.positionY > self.maxY:
              self.positionY = self.maxY
           self.writeNumber(self.mapRangeY(self.maxY))
           self.positionY = self.maxY
           irc.reply('You tilted the camera to the MAXIMUM!!!! ( %d )' %self.positionY)
        else:
           irc.reply('The camera is at its limit ( %d )' %self.positionY)
        irc.reply('The Y position = ( %d )' %self.positionY)
    down = wrap(down, [optional('int')])
    
    def up(self, irc, msg, args, var):
        """< steps >
        HeckBot expects integers."""
        if (self.positionY >= (self.minY - self.incrumentY)):
           self.positionY = self.positionY - self.incrumentY
           if self.positionY < self.minY:
              self.positionY = self.minY
           self.writeNumber(self.mapRangeY(self.positionY))
           irc.reply('You tilted the camera up to ( %d )' %self.positionY)
        elif ((self.positionY >= (self.minY - self.incrumentY)) and (self.positionY > self.minY)):
           if self.positionY < self.minY:
              self.positionY = self.minY
           self.writeNumber(self.mapRangeY(self.minY))
           self.positionY = self.minY
           irc.reply('You tilted the camera to the MINIMUM!!!! ( %d )' %self.positionY)
        else:
           irc.reply('The camera is at its limit ( %d )' %self.positionY)
        irc.reply('The Y position = ( %d )' %self.positionY)
    up = wrap(up, [optional('int')])
    
    def left(self, irc, msg, args, var):
        """< steps >
        HeckBot expects integers."""
        if (self.positionX <= (self.maxX - self.incrumentX)):
           self.positionX = self.positionX + self.incrumentX
           if self.positionX > self.maxX:
              self.positionX = self.maxX
           self.writeNumber(self.mapRangeX(self.positionX))
           irc.reply('You tilted the camera up to ( %d )' %self.positionX)
        elif ((self.positionX >= (self.maxX - self.incrumentX)) and (self.positionX < self.maxX)):
           if self.positionX > self.maxX:
              self.positionX = self.maxX
           self.writeNumber(self.mapRangeX(self.maxX))
           self.positionX = self.maxX
           irc.reply('You tilted the camera to the MAXIMUM!!!! ( %d )' %self.positionX)
        else:
           irc.reply('The camera is at its limit ( %d )' %self.positionX)
        irc.reply('The X position = ( %d )' %self.positionX)
    left = wrap(left, [optional('int')])
    
    def right(self, irc, msg, args, var):
        """< steps >
        HeckBot expects integers."""
        if (self.positionX >= (self.minX - self.incrumentX)):
           self.positionX = self.positionX - self.incrumentX
           if self.positionX < self.minX:
              self.positionX = self.minX
           self.writeNumber(self.mapRangeX(self.positionX))
           irc.reply('You tilted the camera up to ( %d )' %self.positionX)
        elif ((self.positionX >= (self.minX - self.incrumentX)) and (self.positionX > self.minX)):
           if self.positionX < self.minX:
              self.positionX = self.minX
           self.writeNumber(self.mapRangeX(self.minX))
           self.positionX = self.minX
           irc.reply('You tilted the camera to the MINIMUM!!!! ( %d )' %self.positionX)
        else:
           irc.reply('The camera is at its limit ( %d )' %self.positionX)
        irc.reply('The X position = ( %d )' %self.positionX)
    right = wrap(right, [optional('int')])

Class = ShopCam


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
