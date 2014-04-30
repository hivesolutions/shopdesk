#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
import traceback

import appier
import shopify
import easypay
import shopdesk

LOOP_TIMEOUT = 15.0
""" The time value to be used to sleep the main sequence
loop between ticks, this value should not be too small
to spend many resources or to high to create a long set
of time between external interactions """

ORDER_TIMEOUT = 2.0 * 24.0 * 3600.0
""" The default order timeout value that is going to
be used to measure the amount of time before an order
is considered expired and it's canceled """

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
            try:
                self.tick()
            except BaseException as exception:
                self.owner.logger.critical("Unhandled shopdesk exception raised")
                self.owner.logger.error(exception)
                lines = traceback.format_exc().splitlines()
                for line in lines: self.owner.logger.warning(line)
            time.sleep(LOOP_TIMEOUT)

    def stop(self):
        self.running = False

    def tick(self):
        self.check_orders()
        self.cancel_orders()
        self.issue_references()
        self.email_references()

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
            production = appier.conf("EASYPAY_PRODUCTION", cast = bool),
            username = appier.conf("EASYPAY_USERNAME"),
            password = appier.conf("EASYPAY_PASSWORD"),
            cin = appier.conf("EASYPAY_CIN"),
            entity = appier.conf("EASYPAY_ENTITY")
        )
        self.easypay.bind("paid", self.on_paid)
        self.easypay.start_scheduler()

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
            _order = shopdesk.Order.from_shopify(order)
            _order.save()

    def cancel_orders(self):
        expiration = time.time() - ORDER_TIMEOUT
        orders = shopdesk.Order.find(
            payment = shopdesk.Order.ISSUED,
            created = { "$lt" : expiration }
        )
        self.owner.logger.debug("Canceling '%d' outdated orders ..." % len(orders))
        for order in orders: order.cancel_s(self.easypay, self.shopify)

    def issue_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.PENDING)
        self.owner.logger.debug("Issuing references for '%d' orders ..." % len(orders))
        for order in orders: order.issue_reference_s(self.easypay)

    def note_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.ISSUED, note_sent = False)
        self.owner.logger.debug("Noting down '%d' ..." % len(orders))
        for order in orders: order.note_reference_s(self.shopify)

    def email_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.ISSUED, email_sent = False)
        self.owner.logger.debug("Sending emails for '%d' orders ..." % len(orders))
        for order in orders: order.email_reference_s()

    def on_paid(self, reference, details):
        identifier = reference["identifier"]
        order = shopdesk.Order.get(reference_id = identifier, raise_e = False)
        order.pay_s(self.shopify)
