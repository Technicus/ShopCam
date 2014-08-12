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
    _ = PluginInternationalization('IRCI2C')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class IRCI2C(callbacks.Plugin):
    """Add the help for "@plugin help IRCI2C". A plugin that sends stuff to an arduino"""
    # threaded = True 
    pass

    # for RPI version 1, use "bus = smbus.SMBus(0)"
    bus = smbus.SMBus(1)
    # This is the address we setup in the Arduino Program
    address = 0x04

    def writeNumber(self, value):
        self.bus.write_byte(address, value)
        # bus.write_byte_data(address, 0, value)
        return -1

    def readNumber():
        number = self.bus.read_byte(address)
        # number = bus.read_byte_data(address, 1)
        return number

    def i2c(self, irc, msg, args, var):
        """<byte>
        Sends a byte (an integer from 1 to 255) to the arduino."""
        self.writeNumber(var)
        time.sleep(1)
        number = readNumber()
        irc.reply('The Arduino answered: %d' % number)
    i2c = wrap(i2c, ['int'])

Class = IRCI2C


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
