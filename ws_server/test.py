from ws_server.websocket import WSHandler
from ws_server.ssh_connector import SSHConnector
import logging
import os.path

import uuid

import tornado.websocket
from tornado.ioloop import IOLoop

from tornado.options import define, options, parse_command_line

define('address', default='127.0.0.1', help='listen address')
define('port', default=8888, help='listen port', type=int)

BUF_SIZE = 1024
DELAY = 10
base_dir = os.path.dirname(__file__)


class IndexHandler(tornado.web.RequestHandler):
    def get_privatekey(self):
        try:
            return self.request.files.get('privatekey')[0]['body']
        except TypeError:
            pass

    def get_port(self):
        value = self.get_value('port')
        try:
            port = int(value)
        except ValueError:
            port = 0

        if 0 < port < 65536:
            return port

        raise ValueError("Invalid port {}".format(value))

    def get_value(self, name):
        value = self.get_argument(name)
        if not value:
            raise ValueError("Empty {}".format(name))
        return value

    def get_args(self):
        hostname = self.get_value('hostname')
        port = self.get_port()
        username = self.get_value('username')
        password = self.get_argument('password')
        args = (hostname, port, username, password)
        return args

    def get(self):
        self.render('index.html')

    def post(self):
        status = None
        connection = None
        try:
            connection = SSHConnector(*(self.get_args()))
        except Exception as e:
            print('connectFailed {}'.format(e))

        self.write(dict(id=connection.id, status=status))


if __name__ == '__main__':

    settings = {
        'template_path': os.path.join(base_dir, 'templates'),
        'static_path': os.path.join(base_dir, 'static'),
        'cookie_secret': uuid.uuid1().hex,
        'xsrf_cookies': True,
        'debug': True
    }

    handlers = [
        (r'/', IndexHandler),
        (r'/ws', WSHandler)
    ]

    parse_command_line()
    app = tornado.web.Application(handlers, **settings)
    app.listen(options.port, options.address)
    logging.info('Listening on {}:{}'.format(options.address, options.port))
    IOLoop.current().start()