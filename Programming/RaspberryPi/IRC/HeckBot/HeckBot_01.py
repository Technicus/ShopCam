#!/usr/bin/python
# -*- coding: utf8 -*-
 
import socket, string, time, ssl
import urllib, re
 
network = 'chat1.ustream.tv'
nick = 'HeckBot'
chan = 'benheckshopcam'
port = 6697
 
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
def main(network, nick, chan, port):
   socket.connect((network,port))
   irc = ssl.wrap_socket(socket)
   irc.send('NICK %s' % nick)
   print irc.recv(4096)
   irc.send('USER %s %s %s :My bot'  % (nick,nick,nick))
   print irc.recv(4096)
   irc.send('JOIN #%s' % chan)
   print irc.recv(4096)
 
   while True:
      data = irc.recv(4096)
      print data
 
      if data.find('PING') != -1:
         irc.send('PONG '+data.split()[1]+'')
      if data.find('!gtfo') != -1:
         irc.send('QUIT')
         exit()
      print data
 
if __name__=='__main__':
   main(network, nick, chan, port)