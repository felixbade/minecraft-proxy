import socket

import config

class BaseListener:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', config.port))
        self.port = self.socket.getsockname()[1]
    
    def run(self):
        self.socket.listen(5)
        try:
            while True:
                connection, address = self.socket.accept()
                self.new_connection(connection, address)
        except KeyboardInterrupt:
            print()
            self.stop()
        except OSError:
            pass # socket is closed
        finally:
            self.clean_up()

    def stop(self):
        self.socket.close()

    def new_connection(self, connection, address):
        pass

    def clean_up(self):
        pass
