import socket
import _thread
import sys
from Users import CollectionOfUsers

class GuiHandler:
    def __init__(self,socketHandler_):
        self.socketHandler = socketHandler_

    def getPort(self): # server intro GUI to select port for server
        print("Please enter a server port: ")
        self.server_port = input()
        return self.server_port

    def sendMsgBySocketHandlerKicked(self, username):
        self.socketHandler.sendAndShowMsg("Admin kicked the user: " + username)

    def closeConnection(self):
        self.socketHandler.closeEveryThing()

    def showMessage(self,text):
        print(text)

    def sendMsgBySocketHandlerQuit(self):
        self.socketHandler.sendAndShowMsg("Admin is now quiting! Bye!")
        self.closeConnection()

    def showWarningMsg(self):
        print("Couldn't bind port")

class SocketHandler:
    def __init__(self):
        self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creating the server socket, TCP
        self.users = CollectionOfUsers() # the list for user-objects is created
        self.users.readUsersFromFile("server/users.txt") # any previously registered users are loaded from file

    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_

    def closeEveryThing(self): # closing the server
        self.serverSocket.close()
        self.users.writeUsersToFile("server/users.txt") # here: the user-data in RAM is written to file, before closing
        sys.exit(0)

    def startAccepting(self):
        while True:
            try:
                clientSocket, clientAddr = self.serverSocket.accept() # the server waits for connection(s) by client(s)
                self.list_of_unknown_clientSockets.append(clientSocket) # client-sockets are put in a list
                self.list_of_unknown_clientAddr.append(clientAddr)
                self.startReceiverThread(clientSocket, clientAddr)
            except:
                pass

    def startToAcceptConnection(self,port):
        try:
            self.serverSocket.bind(('127.0.0.1',int(port))) # server socket bind to '' (?)
        except:
            return "failed"
        self.serverSocket.listen(9)

        self.list_of_known_usernames = []

        self.list_of_known_clientSockets = []
        self.list_of_known_clientAddr = []

        self.list_of_unknown_clientSockets = []
        self.list_of_unknown_clientAddr = []


        _thread.start_new_thread(self.startAccepting,())
        return "succeed"

    def sendAndShowMsg(self, text): # this function show messages from clients in the server-GUI and forwards to other clients
        if text[0] == "#":
            new_text = text[1:]
            for clientSock in self.list_of_known_clientSockets:
                clientSock.send(str.encode("Admin: " + new_text))
            print(text)

        elif text[:6] == "/close":
            self.closeEveryThing()

        elif text[:5] == "/kick":
            print("/kick")
            user = text[6:]
            for i in range(len(self.list_of_known_usernames)):
                print("In for loop")
                print(user)
                print(self.list_of_known_usernames)
                print(i)
                if self.list_of_known_usernames[i] == user:
                    print(self.list_of_known_usernames)
                    self.list_of_known_usernames.pop(i)
                    self.list_of_known_clientSockets[i].close()
                    print(self.list_of_known_usernames)
                    break

    def startReceiverThread(self, clientSocket, clientAddr): # function to start new thread
        _thread.start_new_thread(self.startReceiving,(clientSocket,clientAddr,))

    def startReceiving(self,clientSocket, clientAddr):
        resultOfLogin = self.listenToUnknownClinet(clientSocket,clientAddr)

        if resultOfLogin !=False:
            username = resultOfLogin
            self.list_of_unknown_clientSockets.remove(clientSocket)
            self.list_of_unknown_clientAddr.remove(clientAddr)
            self.list_of_known_usernames.append(username)
            self.list_of_known_clientSockets.append(clientSocket)
            self.list_of_known_clientAddr.append(clientAddr)

            self.listenToknownClinet(clientSocket,clientAddr,username)

    def listenToUnknownClinet(self,clientSocket, clientAddr):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
            except:
                self.list_of_unknown_clientSockets.remove(clientSocket)
                self.list_of_unknown_clientAddr.remove(clientAddr)
                return False

            args = msg.split(' ')
            if len(args) == 3 and args[0] == "login":
                username = args[1]
                password = args[2]
                if self.users.doesThisUserExistAndNotActive(username,password):
                    clientSocket.send(str.encode("ok"))
                    self.sendAndShowMsg(username + " is connected")
                    return username
                else:
                    clientSocket.send(str.encode("not ok"))

            if len(args) >= 5 and args[0] == "register":
                username = args[1]
                password = args[2]
                email = args[3]
                name = ""
                for rest in args[4:]:
                    name += rest + " "
                if username != "" and password != "" and email != "" and name != "":
                    resultOfAdding = self.users.add_user(username,password,email,name)
                    if resultOfAdding == True:
                        clientSocket.send(str.encode("fine"))
                    else:
                        clientSocket.send(str.encode("not fine"))
                else:
                    clientSocket.send(str.encode("not fine"))

    def listenToknownClinet(self,clientSocket, clientAddr,username):
        while True:
            try:
                msg = clientSocket.recv(1024).decode()
                for clientSock in self.list_of_known_clientSockets:
                    clientSock.send(str.encode(username+": " + msg))
                print(username + ": " + msg)
                # self.sendAndShowMsg(username + ": " + msg)
            except:
                self.list_of_known_clientSockets.remove(clientSocket)
                self.list_of_known_clientAddr.remove(clientAddr)
                self.sendAndShowMsg(username+" disconnected")
                self.users.inactiveUser(username)
                return

    def kickToknownclinet(self, counter_, username_):
        self.counter = counter_
        self.username = username_
        self.list_of_known_clientSockets.pop(self.counter)
        self.list_of_known_clientAddr.pop(self.counter)
        self.list_of_known_usernames.pop(self.counter)
        self.users.inactiveUser(self.username)
