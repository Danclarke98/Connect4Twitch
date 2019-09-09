import socket


PASS = ""
CHANNEL = ""
OWNER = ""
SERVER = "irc.twitch.tv"
PORT = 6667
BOT = "Connect4Twitch"
irc = socket.socket()


#Configuration Parameters
def configure(auth, channel):
    global CHANNEL
    global PASS
    global irc
    global BOT
    PASS = auth
    CHANNEL = channel
    OWNER = channel
    irc.connect((SERVER, PORT))
    irc.send(( "PASS " + PASS + "\n" + 
                "NICK " + BOT + "\n" +
                "JOIN #" + CHANNEL + "\n").encode())


#Join chat using IRC configuration
def joinchat():
    Loading = True
    while Loading:
        readbuffer_join = irc.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        for line in readbuffer_join.split("\n")[0:-1]:
            print(line)
            Loading = loadingComplete(line)

#Check if irc connection is complete        
def loadingComplete(line):
    if ("End of /NAMES list" in line):
        print("Bot has joined " + CHANNEL + "'s Chat")
        sendMessage("Connect4 Connected!")
        return False
    else:
        return True

#Send message to chat
def sendMessage(message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())

#Get message posters username
def getUser(line):
    seperate = line.split(":", 2)
    user = seperate[1].split("!", 1)[0]
    return user

#Get message
def getMessage(line):
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message

#Check if message is from User
def console(line):
    if "PRIVMSG" in line:
        return False
    else:
        return True

#Filter out non vote messages and store valid entries.
def filter(username, vote):
    user = username
    vote = vote
    if vote[0:3] == "!c ":
        choice = vote[3:4]
        try: 
            i = int(choice)
            print("converted: " + str(i))
            #store valid values!!
            if i in range(1,7):
                print("Stored: " + str(i))



        except ValueError:
            print("failed to convert")
    else:
        choice = "Not a choice"
        print(choice)

# Read chat loop
#use timer
def monitorChat():
    while True: 
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""

        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and console(line):
                msgRep = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgRep)
                print(msgRep)
                continue
            else:
                user = getUser(line)
                message = getMessage(line)
                filter(user, message)

# Connect
configure()
joinchat()
monitorChat()



        
