import socket
import _thread

class SocketHandler:
    def __init__(self): # constructor for SocketHandler
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creating socket with ipv4 and TCP

    def setGuiHandler(self,guiHandler_):
        self.guiHandler = guiHandler_

    def connect(self,ip, port):
        try:
            self.clientSocket.connect((ip,int(port))) # trying to connect to server with ip & port
            self.startReceiverThread() # calling other function to start thread
        except:
            return "no connection"

    def sendMsg(self,text):
        try:
            self.clientSocket.send(str.encode(text)) # send text message via client socket, encode to string
        except:
            pass

    def startReceiverThread(self):
        _thread.start_new_thread(self.startReceiving,()) # call to start thread

    def startReceiving(self):
        while True:
            try:
                msg = self.clientSocket.recv(1024).decode() # while loop with recieve message from client(s)
                self.guiHandler.showMessage(msg) # send text message recieved from socket to gui
            except:
                self.guiHandler.showMessage("desconnected...")
                return