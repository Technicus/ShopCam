#!/usr/bin/python
# -*- coding: utf8 -*-
# http://www.devshed.com/c/a/python/python-and-irc/

import socket

network = 'chat1.ustream.tv'
#network = 'irc.freenode.net'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'NICK Spiriticus\r\n' )
irc.send ( 'USER HeckBot HeckBot HeckBot :P HeckBotn IRC\r\n' )
irc.send ( 'JOIN #benheckshopcam\r\n' )
irc.send ( 'PRIVMSG #benheckshopcam :Hello.\r\n' )
while True:
   data = irc.recv ( 4096 )
   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
   elif data.find ( 'PRIVMSG' ) != -1:
      nick = data.split ( '!' ) [ 0 ].replace ( ':', '')
      message = ':'.join ( data.split ( ':' ) [ 2: ] )
      destination = ''.join ( data.split ( ':' ) [ :2 ] ).split ( ' ' ) [ -2 ]
      if destination == 'PyIRC':
         destination = 'PRIVATE'
      print '(', destination, ')', nick + ':', message
   #print data