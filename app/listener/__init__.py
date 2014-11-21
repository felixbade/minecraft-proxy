import logging

from app.listener.base_listener import BaseListener
from app.client import ClientConnection
from app.server_manager import ServerManager

class ClientListener(BaseListener):

    def __init__(self):
        self.manager = ServerManager()
        BaseListener.__init__(self)

    def run(self):
        print('Listening on port: %d' % self.port)
        logging.info('Listening on port: %d' % self.port)
        BaseListener.run(self)
    
    def new_connection(self, connection, address):
        ClientConnection(connection, address, self.manager)

    def clean_up(self):
        logging.info('Stopping application.')
        self.manager.clean_up()
