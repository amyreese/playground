# Copyright 2014 John Reese
# Licensed under the MIT license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from autobahn.asyncio.websocket import (WebSocketServerProtocol,
                                        WebSocketServerFactory)

class TestWebSocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("Websocket connection open")

    def onMessage(self, payload, isbinary):
        if isbinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        self.sendMessage(payload, isbinary)

    def onClose(self, wasclean, code, reason):
        print("Websocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        print('zomg!')
        raise

    factory = WebSocketServerFactory('ws://localhost:9000', debug=True)
    factory.protocol = TestWebSocketProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeybardInterrupt as e:
        print(e)
        pass
    finally:
        server.close()
        loop.close()
