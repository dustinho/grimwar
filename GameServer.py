from twisted.web import server, resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
from Game import *

import json

class GameServer(object):
    """
    Store startup variables that don't belong in Game in here.
    """
    def __init__(self):
        self.readyPlayers = {}

    def registerPlayer(self, id):
        self.readyPlayers[id] = True

    def isReady(self):
        return len(self.readyPlayers) == 2

class RootResource(resource.Resource):
    def __init__(self, game, gameserver):
        self.game = game
        self.gameserver = gameserver
        resource.Resource.__init__(self)
        self.putChild('check', CheckHandler(self.game, self.gameserver))
        self.putChild('new_game', NewGameHandler(self.game, self.gameserver))

class GameResource(resource.Resource):
    def __init__(self, game, gameserver):
        self.game = game
        self.gameserver = gameserver
        resource.Resource.__init__(self)

    def responseFailed(self, err, call):
        call.cancel()


class CheckHandler(GameResource):
    def render_GET(self, request):
        id = request.args['id'][0]
        if id != '1' and id != '2':
            return "Bad ID"

        return json.dumps(self.game, cls=GameEncoder)
"""
TODO - get rid of deque, get rid of player references in the unit.
"""
class GameEncoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, object):
            return super(GameEncoder, self).default(o)
        return o.__dict__

class NewGameHandler(GameResource):
    """
    Async resource.
    @param player (ID of player)
    """
    def render_GET(self, request):
        id = request.args['id'][0]
        if id != '1' and id != '2':
            return "Bad ID"

        self.gameserver.registerPlayer(id)
        call = reactor.callLater(1, self.checkReady, request)
        request.notifyFinish().addErrback(self.responseFailed, call)
        return NOT_DONE_YET

    def checkReady(self, request):
        if self.gameserver.isReady():
            request.write("Ready")
            request.finish()
        else:
            call = reactor.callLater(1, self.checkReady, request)

if __name__ == "__main__":
    import sys
    from twisted.internet import reactor
    game = Game()
    gameserver = GameServer()

    reactor.listenTCP(8080, server.Site(RootResource(game, gameserver)))
    reactor.run()
