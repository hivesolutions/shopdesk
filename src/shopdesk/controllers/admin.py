#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class AdminController(appier.Controller):

    def __init__(self, owner, *args, **kwargs):
        appier.Controller.__init__(self, owner, *args, **kwargs)

    @appier.route("/admin/easypay.json", "GET")
    @appier.ensure("admin")
    def easypay(self):
        return self.scheduler.easypay.diagnostics()
