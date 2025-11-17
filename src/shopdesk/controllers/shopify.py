#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import shopdesk


class ShopifyController(appier.Controller):

    @appier.route("/shopify/order_updated.json", "POST", json=True)
    def order_updated(self):
        object = appier.get_object()
        name = object["name"]
        order = shopdesk.Order.get(s_name=name)
        order.sync_shopify_s()
