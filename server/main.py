from GuiHandler import GuiHandler
from SocketHandler import SocketHandler

socketHandler = SocketHandler()
guiHandler = GuiHandler(socketHandler)
socketHandler.setGuiHandler(guiHandler)

port = guiHandler.getPort()
resultOfBinding = socketHandler.startToAcceptConnection(port)

if resultOfBinding == "failed":
    guiHandler.showWarningMsg()
else:
    guiHandler.startGui()

