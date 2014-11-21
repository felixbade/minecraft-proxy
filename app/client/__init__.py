from threading import Thread
from select import select
import logging
import time

import config
from app.client.minecraft_socket import MinecraftSocket, decodeMCPacket
from app.client import varint
from app.client.heartbeat import HeartBeat

class ClientConnection(Thread):

    def __init__(self, client, address, manager):
        Thread.__init__(self)
        self.client = client
        self.server = None
        self.client_address = address
        self.manager = manager
        self.transmitted_bytes = 0
        self.daemon = True
        self.start()

    def run(self):
        self.mc_client = MinecraftSocket(self.client)
        first_packet = self.mc_client.recv()
        second_packet = self.mc_client.recv()

        if second_packet == b'\x00':
            logging.info('Motd request from %s:%d' % self.client_address)
            self.reply_motd()
            self.stop()

        elif second_packet.startswith(b'\x00'):
            try:
                username = decodeMCPacket(second_packet[1:]).decode()
                if username is None:
                    self.stop()
                    return

                # allow other players to join if the server is already up, but not boot it
                if username not in config.whitelist and not self.manager.is_server_running():
                    logging.info('%s tried to connect to the server from %s:%d but was not whitelisted')
                    self.stop()
                    return
                
                logging.info('%s connected to the server.' % username)
                
                self.heart = HeartBeat(self.client)
                self.manager.register_client(self)
                self.server = self.manager.get_socket_connected_to_server()
                self.heart.stop()
                sent_bytes = self.heart.get_sent_bytes()
                self.mc_server = MinecraftSocket(self.server)
                self.mc_server.send(first_packet)
                self.mc_server.send(second_packet)

                if sent_bytes > 0:
                    # TODO: this does not guarantee to receive all desired data
                    self.server.recv(sent_bytes)
                logging.info('%s joined the game' % username)
                start_time = time.time()

                while True:
                    readable_sockets = select([self.server, self.client], [], [])[0]
                    if self.server in readable_sockets:
                        # TODO: this does not guarantee to send all data
                        data = self.server.recv(4096)
                        self.count_bytes(data)
                        if data == b'':
                            break
                        self.client.send(data)
                    if self.client in readable_sockets:
                        data = self.client.recv(4096)
                        self.count_bytes(data)
                        if data == b'':
                            break
                        self.server.send(data)
            finally:
                self.stop()
                logging.info('%s left the game (play time: %d min, transmitted data: %.1f MB)' % (username, (time.time() - start_time) / 60, self.transmitted_bytes / 1000000))
        else:
            logging.warning(repr(first_packet))
            logging.warning(repr(second_packet))
            logging.warning('Could not decode packets shown above')
            self.stop()

    def reply_motd(self):
        if self.manager.is_server_running():
            description = config.description_online
            max_players = config.max_players_online
        else:
            description = config.description_offline
            max_players = config.max_players_offline
        online_players = self.manager.get_players_online()
        
        data = b'{"description":"' + description.encode() + b'","players":{"max":' + str(max_players).encode() + b',"online":' + str(online_players).encode() + b'},"version":{"name":"1.8","protocol":47}'
        if config.favicon is not None:
            data += b',"favicon":"' + config.favicon + b'"'
        data += b'}'

        data = b'\x00' + varint.encode(len(data)) + data
        self.mc_client.send(data)
        data_to_reply = self.mc_client.recv()
        self.mc_client.send(data_to_reply)

    def stop(self):
        self.client.close()
        if self.server is not None:
            self.server.close()

    def count_bytes(self, data):
        self.transmitted_bytes += len(data)
