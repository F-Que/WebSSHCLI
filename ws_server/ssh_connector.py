import logging
import paramiko
import tornado.websocket
from tornado.ioloop import IOLoop
from tornado.iostream import _ERRNO_CONNRESET
from tornado.util import errno_from_exception

BUF_SIZE = 1024
DELAY = 3


class SSHConnector:
    def __init__(self, host, port, username, password):
        print("start connecting")
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.id = str(id(self))
        self.data = []
        self.handler = None
        self.loop = IOLoop.current()
        self.mode = IOLoop.READ
        try:
            self.ssh.connect(hostname=host, port=port, username=username, password=password)
            self.chan = self.ssh.invoke_shell(term='xterm')
            self.chan.setblocking(0)
            self.fd = self.chan.fileno()
        except Exception as e:
            self.ssh = self.chan = self.fd = None
            print(e)

    def __call__(self, fd, events):
        if events & IOLoop.READ:
            self.read()
        if events & IOLoop.WRITE:
            self.write()
        if events & IOLoop.ERROR:
            self.close()

    def set_handler(self, handler):
        if not self.handler:
            self.handler = handler

    def update_handler(self, mode):
        if self.mode != mode:
            self.loop.update_handler(self.fd, mode)
            self.mode = mode

    def read(self):
        print('Connection {} read'.format(self.id))
        try:
            data = self.chan.recv(BUF_SIZE)
        except Exception as e:
            print(e)
            if errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close()
        else:
            print('"{}" from {}'.format(data, self.host))
            if not data:
                self.close()
                return

            print('"{}" to {}'.format(data, self.handler.src_addr))
            try:
                self.handler.write_message(data)
            except tornado.websocket.WebSocketClosedError:
                self.close()

    def write(self):
        logging.debug('Connection {} write'.format(self.id))
        if not self.data:
            return

        data = ''.join(self.data)
        print('"{}" to {}'.format(data, self.host))

        try:
            sent = self.chan.send(data)
        except (OSError, IOError) as e:
            logging.error(e)
            if errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close()
            else:
                self.update_handler(IOLoop.WRITE)
        else:
            self.data = []
            data = data[sent:]
            if data:
                self.data.append(data)
                self.update_handler(IOLoop.WRITE)
            else:
                self.update_handler(IOLoop.READ)

    def close(self):
        print('Closing connection {}'.format(self.id))
        if self.handler:
            self.loop.remove_handler(self.fd)
            self.handler.close()
        self.chan.close()
        self.ssh.close()
        print('Connection to {} closed'.format(self.host))
