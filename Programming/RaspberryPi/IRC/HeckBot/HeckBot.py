# Developing a Basic IRC Bot with Python
# http://forum.codecall.net/topic/59608-developing-a-basic-irc-bot-with-python/


# FIrst We need to do an import for the socket library to do this we use the import command
import socket

# We need to have some variables to tell the Bot what its called and where it is going. To do this we use something similar to the following
nick = 'HeckBot' #define nick
debug = False # For debug Mode
network = 'chat1.ustream.tv' #Define IRC Network
port = 6667 #Define IRC Server Port


# Now we need to setup our debug mode. To do so we will use an IF statement. This will Check if debug is true or false and give the appropriate channel.
if debug == True: #Check if Debug is True
    chan = '#bottesting'
elif debug == False: #Check if debus is false
    chan = '#benheckshopcam'

# Next we need to connect to the server. We need to define our socket also.
# When Defining our socket we will use AF_INET.
# To define our socket we make a variable and define the socket in the variable. Our variable will be called "irc"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Define  IRC Socket

# Now to make it connect it is VERY simple. It will just be "irc.connect"
irc.connect((network,port)) #Connect to Server

# Now we setup a Receive buffer and send some data
# Setting up the Receive buffer uses the irc.recv command
# Sending Data uses the irc.send command.
# N.B : The data we are sending is simple IRC Protocol
#data = irc.recv(4096)
#irc.recv (4096) #Setting up the Buffer
irc.send('NICK ' + nick + '\r\n') #Send our Nick(Notice the Concatenation)
irc.send('USER HeckBot HeckBot HeckBot :HeckB IRC\r\n') #Send User Info to the server
data = ircRecv() # explained later
if data.find('PING') != -1:
    ircSend('PONG ' + data.split()[1] + '\r\n')
irc.send('JOIN ' + chan + '\r\n') # Join the pre defined channel
irc.send('PRIVMSG ' + chan + ' :Hello.\r\n') #Send a Message to the  channel

# Now we have our Basic IRC Setup Try the Script so Far.
# To Keep our bot from pinging out We will introduce a while statement to handle IRC Pings. To do so we will add The following code
while True: #While Connection is Active
   data = irc.recv (4096) #Make Data the Receive Buffer
   print data #Print the Data to the console(For debug purposes)
   if data.find('PING') != -1: #If PING is Found in the Data
      irc.send('PONG ' + data.split()[1] + '\r\n') #Send back a PONG

# Again most of the above is Basic IRC Protocol.
# Now we will start to add commands to do this we must split the strings. Add the following under the last IF
   elif data.find('PRIVMSG') != -1: #IF PRIVMSG is in the Data Parse it
      message = ':'.join(data.split (':')[2:]) #Split the command from the message
      if message.lower().find('TheDefaced') == -1: #If TheDefaced(Change to Suit Chan name) is in the message continue
        nick = data.split('!')[ 0 ].replace(':',' ') #The nick of the user issueing the command is taken from the hostname
        destination = ''.join (data.split(':')[:2]).split (' ')[-2] #Destination is taken from the data
        function = message.split( )[0] #The function is the message split
        print 'Funtion is ' + function + ' From ' + nick #Print who commanded [This is for debug and logging]
        arg = data.split( ) #FInally Split the Arguments by space (arg[0] will be the actual command

# Ok the following is a waste of code but as I say I am learning. This snippet will take all the args from the command its here for the say function. Add it under the variable arg.
args = '' #Create the Variable for use
for index,item in enumerate(arg) : #For every index and item in arg
   if index > 3 : # If the index is Greater than 3
      if args == '': # If there are no Current Args
         args = item #Make Item the First Argument
      else : #Else
         args += ' ' + item #Add the item to the  sting

# Now we are almost done. We just need to add some commands .
# The following command is a fairly simple command. It just prints out something to the IRC.
   if function == 'Author\r\n': #If function is Equal to Author
      irc.send('PRIVMSG ' + chan + ' :' + nick + ' I am Coded By  Affix\r\n') #Print the Author

# Again the above is Basic IRC
# The Say command is DIfferent. It uses a group of Arguments (the args variable we made earlier)
if function == 'say': #Get the command Say
             irc.send('PRIVMSG ' + chan + ' :' + args + '\r\n') #Print What you want it to say (Note the ARGS)

# Simple Huh?
# Now if we want to use multiple arguments
if function == 'arguments':
             irc.send('PRIVMSG ' + chan + ' :' + arg[1] + arg[2] +  '\r\n') #Print out only Arguments 1 and two
             
# Well the above command will only print the first 2 arguments. Again basic IRC Protocol[/code]
# Thats it for my Tutorial on a Basic Python IRC bot. Hope you enjoyed it. Any comments please post. 

