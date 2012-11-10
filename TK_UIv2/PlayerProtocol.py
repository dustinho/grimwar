
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

from PlayerInputs import PlayCard 

class PlayerProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        self.factory.callback(data)
        

class PlayerProtocolFactory(Factory):
    def __init__(self, dataReceivedCallback):
        self.callback = dataReceivedCallback

    def buildProtocol(self, addr):
        return PlayerProtocol(self)


if __name__ == "__main__":
    def connectionCallback(p):
        pass
        p.sendMessage("Hello")

    def printCallback(data):
        print data

    point = TCP4ClientEndpoint(reactor, "localhost", 1079)
    d = point.connect(ObserverFactory(printCallback))
    d.addCallback(connectionCallback)
    reactor.run()
