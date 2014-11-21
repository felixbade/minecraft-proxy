from threading import Thread
import time

class HeartBeat(Thread):

    def __init__(self, s):
        self.data = b'\xab\x01\x01\x00\xa2\x010\x81'
        self.socket = s
        self.sent_bytes = 0
        self.heartbeat_time = 10
        self.stopped = False
        
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        time.sleep(self.heartbeat_time)
        while not self.stopped:
            self.send_heartbeat()
            time.sleep(self.heartbeat_time)

    def send_heartbeat(self):
        self.last_data = time.time()
        self.socket.send(self.data[0:1])
        self.sent_bytes += 1
        self.data = self.data[1:]

    def stop(self):
        self.stopped = True

    def get_sent_bytes(self):
        return self.sent_bytes
