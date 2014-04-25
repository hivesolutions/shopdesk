#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading

LOOP_TIMEOUT = 15.0

class Scheduler(threading.Thread):
    """
    Scheduler class that handles all the async tasks
    relates with the house keeping of the shopdesk
    infra-structure. The architecture of the logic
    for the class should be modular in the sense that
    new task may be added to it through a queue system.
    """

    def __init__(self, api):
        threading.Thread.__init__(self)
        self.api = api
        self.daemon = True

    def run(self):
        self.running  = True
        while self.running:
            self.tick()
            time.sleep(LOOP_TIMEOUT)

    def stop(self):
        self.running = False

    def tick(self):
        pass
