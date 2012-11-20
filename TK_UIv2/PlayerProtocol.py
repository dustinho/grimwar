
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint

from PlayerInputs import PlayCard 

class PlayerProtocol(NetstringReceiver):
    def __init__(self, factory):
        self.factory = factory

    def stringReceived(self, string):
        self.factory.callback(string)
        

class PlayerProtocolFactory(Factory):
    def __init__(self, dataReceivedCallback):
        self.callback = dataReceivedCallback

    def buildProtocol(self, addr):
        return PlayerProtocol(self)


if __name__ == "__main__":
    def connectionCallback(p):
        pass
        p.sendString("Hello")

    def printCallback(data):
        print data

    point = TCP4ClientEndpoint(reactor, "localhost", 1079)
    d = point.connect(ObserverFactory(printCallback))
    d.addCallback(connectionCallback)
    reactor.run()
