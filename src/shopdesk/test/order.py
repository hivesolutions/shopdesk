#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest

import appier

import shopdesk

class OrderTest(unittest.TestCase):

    def setUp(self):
        self.app = shopdesk.ShopdeskApp(level = logging.ERROR)

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

    def test_shopify(self):
        order = dict(
            id = 1,
            name = "name",
            total_price = "20.00",
            currency = "EUR",
            created_at = "2019-01-01T17:00:00+01:00",
            financial_status = "pending",
            fulfillment_status = "partial",
            email = "username@domain.com",
            billing_address = dict(name = "name"),
        )
        transaction = dict(gateway = "mb")
        order = shopdesk.Order.from_shopify(order, transactions = [transaction])

        self.assertEqual(order.s_id, 1)
        self.assertEqual(order.s_name, "name")
        self.assertEqual(order.s_total_price, "20.00")
        self.assertEqual(order.s_currency, "EUR")
        self.assertEqual(order.s_created_at, "2019-01-01T17:00:00+01:00")
        self.assertEqual(order.s_status, "pending")
        self.assertEqual(order.s_fulfillment, "partial")
        self.assertEqual(order.s_email, "username@domain.com")
        self.assertEqual(order.s_billing_name, "name")
        self.assertEqual(order.s_gateway, "mb")
        self.assertEqual(order.payment, shopdesk.Order.UNSET)
        self.assertEqual(order.note_sent, False)
        self.assertEqual(order.email_sent, False)
        self.assertEqual(order.warning_sent, False)

        order.save()

        self.assertEqual(order.s_id, 1)
        self.assertEqual(order.s_name, "name")
        self.assertEqual(order.s_total_price, "20.00")
        self.assertEqual(order.s_currency, "EUR")
        self.assertEqual(order.s_created_at, "2019-01-01T17:00:00+01:00")
        self.assertEqual(order.s_status, "pending")
        self.assertEqual(order.s_fulfillment, "partial")
        self.assertEqual(order.s_email, "username@domain.com")
        self.assertEqual(order.s_billing_name, "name")
        self.assertEqual(order.s_gateway, "mb")
        self.assertEqual(order.payment, shopdesk.Order.PAID)
        self.assertEqual(order.note_sent, False)
        self.assertEqual(order.email_sent, False)
        self.assertEqual(order.warning_sent, False)
