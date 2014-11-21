import time
import socket
import logging

from app.server_manager.ec2 import EC2Client
from app.server_manager.shutdown_timer import ShutdownTimer
import config

class ServerManager:

    def __init__(self):
        self.ec2_conn = EC2Client()
        self.timer = ShutdownTimer(self)
        self.players = []

    def get_socket_connected_to_server(self):
        self.boot_and_wait()
        ip = self.ec2_conn.get_ip()
        port = config.minecraft_server_port
        address = (ip, port)
        logging.debug('Server address: %s:%d' % address)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((ip, port))
            except ConnectionRefusedError:
                logging.debug('Connection refused to the server')
                time.sleep(1)
            except ConnectionAbortedError:
                logging.debug('Connection aborted to the server')
            else:
                logging.debug('Connected to the server')
                return s

    def boot_and_wait(self):
        while True:
            status = self.ec2_conn.get_status()
            if status == 'running':
                return
            if status == 'stopped':
                self.ec2_conn.start()
                self.timer.stop() # just in case, might be useless
                self.timer = ShutdownTimer(self)
            time.sleep(0.1) # some non-zero time to prevent flooding

    def clean_up(self):
        self.terminate_all_clients()
        self.shutdown()

    def shutdown(self):
        self.ec2_conn.stop()
        self.timer.stop()
    
    def terminate_all_clients(self):
        print('Terminating all client connections.')
        for client in self.players:
            client.stop()

    def is_server_running(self):
        return self.ec2_conn.get_status() == 'running'

    def can_server_shutdown(self):
        return self.get_players_online() == 0

    def get_players_online(self):
        for player in self.players:
            if not player.isAlive():
                self.players.remove(player)
        count = len(self.players)
        logging.debug('Players online: %d' % count)
        return count

    def register_client(self, client):
        if not client in self.players:
            self.players.append(client)
