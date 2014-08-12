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
    
    pan = 0
    tilt = 0
    panCenter = 63
    tiltCenter = 191

    def writeNumber(self, value):
        self.bus.write_byte(self.address, value)
        # bus.write_byte_data(address, 0, value)
        return -1

    def readNumber(self):
        # number = 0
        self.bus.write_byte(self.address, number)
        # number = bus.read_byte_data(address, 1)
        return number

    def move(self, irc, msg, args, var):
        """<byte>
        Sends a byte (an integer from 1 to 255) to the arduino."""
        # number = 0
        self.writeNumber(var)
        time.sleep(1)
        number = self.readNumber()
        irc.reply('The Arduino answered: %d' % number)
    move = wrap(move, ['int'])
    
    def up(self, irc, msg, args, var):
        """<byte>
        Sends a byte (an integer from 1 to 255) to the arduino."""
        # number = 0
        self.writeNumber(var)
        time.sleep(1)
        number = self.readNumber()
        irc.reply('The Arduino answered: %d' % number)
    up = wrap(up, ['int'])
    
    def down(self, irc, msg, args, var):
        """<byte>
        Sends a byte (an integer from 1 to 255) to the arduino."""
        # number = 0
        self.writeNumber(var)
        time.sleep(1)
        number = self.readNumber()
        irc.reply('The Arduino answered: %d' % number)
    down = wrap(down, ['int'])
    
    def left(self, irc, msg, args, var):
        """<byte>
        Sends a byte (an integer from 1 to 255) to the arduino."""
        # number = 0
        self.writeNumber(var)
        time.sleep(1)
        number = self.readNumber()
        irc.reply('The Arduino answered: %d' % number)
    left = wrap(left, ['int'])
    
    def right(self, irc, msg, args, var):
        """<byte>
        Sends a byte (an integer from 1 to 255) to the arduino."""
        # number = 0
        self.writeNumber(var)
        time.sleep(1)
        number = self.readNumber()
        irc.reply('The Arduino answered: %d' % number)
    right = wrap(right, ['int'])

Class = ShopCam


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
