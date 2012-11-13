from twisted.internet import protocol

class ServerProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.onConnection(self)

    def connectionLost(self, reason):
        self.factory.onLost(self, reason)

    def sendData(self, data):
        self.transport.write(data)

    def dataReceived(self, data):
        self.factory.onReceived(data)


class ServerProtocolFactory(protocol.ServerFactory):
    def __init__(self, onConnection, onReceived):
        self.onConnection = onConnection
        self.onReceived = onReceived
        self.connections = []

    def buildProtocol(self, addr):
        print addr
        protocol = ServerProtocol(self)
        self.connections.append(protocol)
        return protocol

    def getConnectionCount(self):
        return len(self.connections)

    def onLost(self, protocol, reason):
        self.connections.remove(protocol)

    def broadcast(self, msg):
        for conn in self.connections:
            conn.sendData(msg)



