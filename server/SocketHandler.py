import socket
import _thread
import sys
from Users import CollectionOfUsers

class GuiHandler:
    def __init__(self,socketHandler_):
        self.socketHandler = socketHandler_

    def getPort(self): # server intro GUI to select port for server
        lab = input("Please enter a port to start the server with:\n")
        self.portToReturn = ""
        self.portToReturn = lab
        return self.portToReturn

    def startMainGui(self): # main graphical window for chat server
        self.server_input = input(": ")
        if self.server_input == "/quit":
            self.closeConnection()
        if self.server_input == "/kick":
            self.closeConnection()
        else:
            self.sendMsgBySocketHandler()

    def sendMsgBySocketHandler(self):
        self.socketHandler.sendAndShowMsg("Admin: " + self.server_input)

    def closeConnection(self):
        self.socketHandler.closeEveryThing()

    def startGui(self):
        self.startMainGui()

    def showMessage(self,text):
        print(text)

    def showWarningMsg(self):
        print("Couldn't bind port")

class SocketHandler:
    def __init__(self):
        self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creating the server socket, TCP
        self.users = CollectionOfUsers() # the list for user-objects is created
        self.users.readUsersFromFile() # any previously registered users are loaded from file

    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_

    def closeEveryThing(self): # closing the server
        self.serverSocket.close()
        self.users.writeUsersToFile() # here: the user-data in RAM is written to file, before closing
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
            self.serverSocket.bind(('',int(port))) # server socket bind to '' (?)
        except:
            return "failed"
        self.serverSocket.listen(9)

        self.list_of_known_clientSockets = []
        self.list_of_known_clientAddr = []

        self.list_of_unknown_clientSockets = []
        self.list_of_unknown_clientAddr = []

        _thread.start_new_thread(self.startAccepting,())
        return "succeed"

    def sendAndShowMsg(self, text): # this function show messages from clients in the server-GUI and forwards to other clients
        self.guiHandler.showMessage(text)
        for clientSock in self.list_of_known_clientSockets:
            clientSock.send(str.encode(text))

    def startReceiverThread(self, clientSocket, clientAddr): # function to start new thread
        _thread.start_new_thread(self.startReceiving,(clientSocket,clientAddr,))

    def startReceiving(self,clientSocket, clientAddr):
        resultOfLogin = self.listenToUnknownClinet(clientSocket,clientAddr)

        if resultOfLogin !=False:
            username = resultOfLogin
            self.list_of_unknown_clientSockets.remove(clientSocket)
            self.list_of_unknown_clientAddr.remove(clientAddr)

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
                self.sendAndShowMsg(username + ": " + msg)
            except:
                self.list_of_known_clientSockets.remove(clientSocket)
                self.list_of_known_clientAddr.remove(clientAddr)
                self.sendAndShowMsg(username+" disconnected")
                self.users.inactiveUser(username)
                return
