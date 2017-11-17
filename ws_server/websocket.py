import logging

import weakref

import tornado.websocket
from tornado.ioloop import IOLoop

from .ssh_connector import SSHConnector


class WSHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        self.src_addr = None
        self.loop = IOLoop.current()
        self.con_ref = None
        super(self.__class__, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    '''def open(self):
        self.src_addr = '{}:{}'.format(*self.stream.socket.getpeername())
        print('Connected from {}'.format(self.src_addr))
        connection = SSHConnector.connections.pop(self.get_argument('id'), None)
        if not connection:
            self.close(reason='Invalid connection id')
            return
        self.set_nodelay(True)
        connection.set_handler(self)
        self.con_ref = weakref.ref(connection)
        self.loop.add_handler(connection.fd, connection, IOLoop.READ)'''

    def open(self):

        self.src_addr = '{}:{}'.format(*self.stream.socket.getpeername())
        print('Connected from {}'.format(self.src_addr))
        connection = self.start_ssh_connect()
        if connection is None:
            self.close(reason='Failed to connect to {}'.format(connection.host))
        self.con_ref = weakref.ref(connection)
        self.loop.add_handler(connection.fd, connection, IOLoop.READ)

    def on_message(self, message):
        print('"{}" from {}'.format(message, self.src_addr))
        connection = self.con_ref()
        connection.data.append(message)
        connection.write()

    def on_close(self):
        logging.info('Disconnected from {}'.format(self.src_addr))
        connection = self.con_ref() if self.con_ref else None
        if connection:
            connection.close()

    def data_received(self, chunk):
        pass

    def start_ssh_connect(self):
        print(self.get_argument('host'))
        args = (self.get_argument('host'),
                int(self.get_argument('port')),
                self.get_argument('username'),
                self.get_argument('password'))
        connection = SSHConnector(*args)
        if connection.ssh is None:
            return None
        else:
            connection.set_handler(self)
        return connection