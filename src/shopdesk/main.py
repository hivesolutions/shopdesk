#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

from shopdesk import scheduler

class ShopdeskApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(
            self,
            name = "shopdesk",
            parts = (
                appier_extras.AdminPart,
            )
        )
        self.scheduler = scheduler.Scheduler(self)

    def start(self):
        appier.WebApp.start(self)
        self.scheduler.start()

if __name__ == "__main__":
    app = ShopdeskApp()
    app.serve()
