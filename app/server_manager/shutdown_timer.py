import logging
import time
from threading import Thread

perioid_length = 60*60
shutdown_time_before_perioid_end = 2*60

class ShutdownTimer(Thread):

    def __init__(self, server):
        self.server = server
        self.stopped = False
        self.last_server_boot_time = time.time()
        
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            t = self.get_time_to_next_shutdown_test()
            time.sleep(self.get_time_to_next_shutdown_test())
            if self.stopped:
                break
            if self.server.can_server_shutdown():
                logging.info('No players online, shutting server down')
                self.server.shutdown()

    def get_time_to_next_shutdown_test(self):
        # TODO: this method is really hard to read
        time_from_start = time.time() - self.last_server_boot_time
        perioids_from_start = (time_from_start + shutdown_time_before_perioid_end) // perioid_length
        next_perioid_uptime = (perioids_from_start + 1) * perioid_length
        time_at_next_perioid = self.last_server_boot_time + next_perioid_uptime
        time_to_next_perioid = time_at_next_perioid - time.time()
        return time_to_next_perioid - shutdown_time_before_perioid_end

    def stop(self):
        self.stopped = True
