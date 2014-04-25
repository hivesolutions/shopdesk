#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading

import appier
import shopify
import easypay
import shopdesk

LOOP_TIMEOUT = 60.0

class Scheduler(threading.Thread):
    """
    Scheduler class that handles all the async tasks
    relates with the house keeping of the shopdesk
    infra-structure. The architecture of the logic
    for the class should be modular in the sense that
    new task may be added to it through a queue system.
    """

    def __init__(self, owner):
        threading.Thread.__init__(self)
        self.owner = owner
        self.daemon = True

    def run(self):
        self.running  = True
        self.load()
        while self.running:
            self.tick()
            time.sleep(LOOP_TIMEOUT)

    def stop(self):
        self.running = False

    def tick(self):
        self.check_orders()
        self.issue_references()

    def load(self):
        self.load_shopify()
        self.load_easypay()

    def load_shopify(self):
        self.shopify = shopify.Api(
            api_key = appier.conf("SHOPIFY_API_KEY"),
            password = appier.conf("SHOPIFY_PASSWORD"),
            secret = appier.conf("SHOPIFY_SECRET"),
            store_url = appier.conf("SHOPIFY_STORE")
        )

    def load_easypay(self):
        self.easypay = easypay.ShelveApi(
            username = appier.conf("EASYPAY_USERNAME"),
            password = appier.conf("EASYPAY_PASSWORD"),
            cin = appier.conf("EASYPAY_CIN"),
            entity = appier.conf("EASYPAY_ENTITY")
        )
        self.easypay.bind("paid", self.on_paid)

    def check_orders(self):
        self.owner.logger.debug("Checking shopify orders ...")
        orders = self.shopify.list_orders(limit = 30)
        new_orders = []
        for order in orders:
            _order = shopdesk.Order.get(s_id = order["id"], raise_e = False)
            if _order: continue
            new_orders.append(order)
        self.owner.logger.debug("Found '%d' new shopify orders", len(new_orders))
        for order in new_orders:
            _order = shopdesk.Order(
                s_id = order["id"],
                s_name = order["name"],
                s_total_price = order["total_price"],
                s_gateway = order["gateway"],
                s_status = order["financial_status"]
            )
            _order.save()

    def issue_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.PENDING)
        self.owner.logger.debug("Issuing references for '%d' orders ..." % len(orders))
        for order in orders:
            amount = float(order.s_total_price)
            reference = self.easypay.generate_mb(amount)
            order.reference = reference["identifier"]
            order.payment = shopdesk.Order.ISSUED
            order.save()

    def on_paid(self, reference, details):
        identifier = reference["identifier"]
        order = shopdesk.Order.get(reference = identifier, raise_e = False)
        self.owner.logger.debug("Received payment for order '%s'" % order.name)
        #@todo should trigger an event fo email notification
