#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class ShopdeskApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(
            self,
            name = "shopdesk"
        )

if __name__ == "__main__":
    app = ShopdeskApp()
    app.serve()
