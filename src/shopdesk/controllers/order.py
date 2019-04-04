#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import easypay

import shopdesk

class OrderController(appier.Controller):

    @appier.route("/orders/generate_mb.json", "GET", json = True)
    @appier.ensure(token = "admin")
    def generate_mb_json(self):
        amount = self.field("amount", "10.0")
        easypay = self.get_easypay()
        reference = easypay.generate_mb(amount)
        return reference

    @appier.route("/orders/ctt.csv", "GET")
    @appier.ensure(token = "admin")
    def ctt_csv(self):
        paid = self.field("paid", True, cast = bool)
        sms = self.field("sms", False, cast = bool)
        quantity = self.field("quantity", 1, cast = int)
        object = appier.get_object(
            alias = True,
            find = True,
            limit = 0,
            sort = [("id", -1)]
        )
        if paid: object["payment"] = shopdesk.Order.PAID
        orders = self.admin_part._find_view(shopdesk.Order, **object)
        orders_s = []
        for order in orders:
            order.quantity = 12 #@ todo get the quantity from the lines
            s_shipping_zip = order.s_shipping_zip or ""
            if not "-" in s_shipping_zip: s_shipping_zip += "-"
            weight = "%.2f" % (order.quantity * 100)
            weight = weight.replace(".", ",")
            line = dict(
                reference = order.s_name,
                quantity = int(order.quantity) if quantity == None else quantity,
                weight = weight,
                price = "0ue",
                destiny = order.s_shipping_name[:60],
                title = "",
                name = order.s_shipping_name[:60],
                address = order.s_shipping_street[:60],
                town = order.s_shipping_city[:50],
                zip_code_4 = s_shipping_zip.split("-", 1)[0][:4],
                zip_code_3 = s_shipping_zip.split("-", 1)[1][:3],
                not_applicable_1 = "",
                observations = "",
                back = 0,
                document_code = "",
                phone_number = "",
                saturday = 0,
                email = (order.s_email or "")[:200],
                country = order.s_shipping_country_code,
                fragile = 0,
                not_applicable_2 = "",
                document_collection = "",
                code_email = "",
                mobile_phone = "",
                second_delivery = 0,
                delivery_date = "",
                return_signed_document = 0,
                expeditor_instructions = 0,
                sms = 1 if sms else 0,
                not_applicable_3 = "",
                printer = "",
                ticket_machine = "",
                at_code = ""
            )
            order_s = (
                line["reference"],
                str(line["quantity"]),
                line["weight"],
                line["price"],
                line["destiny"],
                line["title"],
                line["name"],
                line["address"],
                line["town"],
                line["zip_code_4"],
                line["zip_code_3"],
                line["not_applicable_1"],
                line["observations"],
                str(line["back"]),
                line["document_code"],
                line["phone_number"],
                str(line["saturday"]),
                line["email"],
                line["country"],
                str(line["fragile"]),
                line["not_applicable_2"],
                line["document_collection"],
                line["code_email"],
                line["mobile_phone"],
                str(line["second_delivery"]),
                line["delivery_date"],
                str(line["return_signed_document"]),
                str(line["expeditor_instructions"]),
                str(line["sms"]),
                line["not_applicable_3"],
                line["printer"],
                line["ticket_machine"],
                line["at_code"]
            )
            orders_s.append(order_s)
        result = appier.serialize_csv(
            orders_s,
            encoding = "Cp1252",
            errors = "ignore",
            delimiter = "+"
        )
        result = appier.legacy.bytes(
            result,
            encoding = "Cp1252",
            errors = "ignore"
        )
        self.content_type("text/csv")
        return result

    def get_easypay(self):
        return easypay.API()
