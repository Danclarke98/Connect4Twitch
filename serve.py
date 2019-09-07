import socket

#Configuration Parameters
SERVER = "irc.twitch.tv"
PORT = 6667
PASS = ""
BOT = "Connect4Twitch"
CHANNEL = ""
OWNER = ""
irc = socket.socket()
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
        sendMessage(irc, "Connect4 Connected!")
        return False
    else:
        return True

#Send message to chat
def sendMessage(irc, message):
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

#Filter out non vote messages and store.
def filter(username, vote):
    user = username
    vote = vote
    if vote[0:3] == "!c ":
        choice = vote[3:4]
    else:
        choice = ""


# Connect
joinchat()

# Read chat loop
while True: 
    try:
        readbuffer = irc.recv(1024).decode()
    except:
        readbuffer = ""

    for line in readbuffer.split("\r\n"):
        if line == "":
            continue
        else:
            user = getUser(line)
            message = getMessage(line)
            filter(user, message)
        if "PING" in line and console(line):
            msgRep = "PONG tmi.twitch.tv\r\n".encode()
            irc.send(msgRep)
            print(msgRep)
            continue
