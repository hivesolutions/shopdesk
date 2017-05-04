#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import easypay

class OrderController(appier.Controller):

    @appier.route("/orders/generate_mb.json", "GET", json = True)
    @appier.ensure("admin")
    def generate_mb_json(self):
        amount = self.field("amount", "10.0")
        easypay = self.get_easypay()
        reference = easypay.generate_mb(amount)
        return reference

    def get_easypay(self):
        return easypay.Api()
