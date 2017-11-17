from ws_server.websocket import WSHandler
import tornado.web
from tornado.ioloop import IOLoop

HOST = '0.0.0.0'
WS_PORT = '5001'

if __name__ == "__main__":
    handlers = [(r'/ws', WSHandler)]
    settings = {'debug': True}
    ws_server = tornado.web.Application(handlers, **settings)
    ws_server.listen(WS_PORT, HOST)
    print('WebSocket server start on {}:{}'.format(HOST, WS_PORT))
    IOLoop.current().start()