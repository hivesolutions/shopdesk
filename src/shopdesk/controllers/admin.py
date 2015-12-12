#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import appier
import appier_extras

class AdminController(appier.Controller):

    @appier.route("/admin/easypay.json", "GET")
    @appier.ensure("admin")
    def easypay(self):
        return self.scheduler.easypay.diagnostics()

    @appier.route("/admin/email.json", "GET")
    @appier.ensure("admin")
    def email_test(self):
        email = self.field("email", None)
        if not email: raise appier.OperationalError(
            message = "No email defined"
        )
        base = appier_extras.admin.Base()
        base.send_email(
            "email/test.html.tpl",
            receivers = [email],
            subject = self.to_locale("Shopdesk test email")
        )
        return dict(email = email)

    @appier.route("/admin/shelve", "GET")
    @appier.ensure("admin")
    def export_shelve(self):
        shelve_path = self.scheduler.easypay.path
        shelve_path = os.path.abspath(shelve_path)
        return self.send_path(shelve_path)
