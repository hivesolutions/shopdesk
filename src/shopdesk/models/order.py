#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

class Order(appier_extras.admin.Base):

    PENDING = 1
    ISSUED = 2
    PAID = 3
    CANCELED = 4
    REFUNDED = 5
    OTHER = 6

    PAYMENT_S = {
        PENDING : "pending",
        ISSUED : "issued",
        PAID : "paid",
        CANCELED : "canceled",
        REFUNDED : "refunded",
        OTHER : "other"
    }

    VALID_PAYMENTS = ("Multibanco",)

    s_id = appier.field(
        type = int,
        index = True,
        immutable = True,
        default = True
    )

    s_name = appier.field(
        index = True,
        immutable = True
    )

    s_total_price = appier.field(
        index = True,
        immutable = True
    )

    s_currency = appier.field(
        index = True,
        immutable = True
    )

    s_gateway = appier.field(
        index = True,
        immutable = True
    )

    s_status = appier.field(
        index = True,
        immutable = True
    )

    s_email = appier.field(
        index = True,
        immutable = True
    )

    s_billing_name = appier.field(
        index = True,
        immutable = True
    )

    payment = appier.field(
        type = int,
        safe = True,
        index = True,
        meta = "enum",
        enum = PAYMENT_S
    )

    email_sent = appier.field(
        type = bool,
        safe = True,
        index = True
    )

    entity = appier.field(
        index = True
    )

    reference = appier.field(
        index = True
    )

    @classmethod
    def validate(cls):
        return super(Order, cls).validate() + [
            appier.not_null("s_id"),

            appier.not_null("s_name"),
            appier.not_empty("s_name"),

            appier.not_null("s_total_price"),

            appier.not_null("s_status"),

            appier.not_null("payment")
        ]

    @classmethod
    def from_shopify(cls, order):
        return cls(
            s_id = order["id"],
            s_name = order["name"],
            s_total_price = order["total_price"],
            s_currency = order["currency"],
            s_gateway = order["gateway"],
            s_status = order["financial_status"],
            s_email = order["email"],
            s_billing_name = order["billing_address"]["name"],
            email_sent = False
        )

    def pre_validate(self):
        appier_extras.admin.Base.pre_validate(self)

        self.start_payment()

    def start_payment(self):
        if hasattr(self, "payment"): return
        if not hasattr(self, "s_status") : return
        if not hasattr(self, "s_gateway") : return
        if not self.s_gateway in Order.VALID_PAYMENTS: self.payment = Order.PAID; return
        if self.s_status == "pending": self.payment = Order.PENDING; return
        if self.s_status == "refunded": self.payment = Order.REFUNDED; return
        self.payment = Order.PAID

    def issue_reference_s(self, easypay):
        amount = float(self.s_total_price)
        reference = easypay.generate_mb(amount)
        self.entity = reference["entity"]
        self.reference = reference["identifier"]
        self.payment = Order.ISSUED
        self.save()
        self.owner.logger.debug("Issued reference for order '%s'" % self.s_name)

    def pay_s(self, shopify):
        shopify.pay_order(self.s_id)
        self.payment = Order.PAID
        self.save()
        self.owner.logger.debug("Received payment for order '%s'" % self.s_name)

    def cancel_s(self, easypay, shopify):
        easypay.cancel_mb(self.reference)
        shopify.cancel_order(self.s_id)
        self.payment = Order.CANCELED
        self.save()
        self.owner.logger.debug("Canceled and reversed order '%s'" % self.s_name)

    def email_reference_s(self):
        self.send_email(
            "email/reference.html.tpl",
            receivers = [self.email_mime()],
            subject = self.to_locale("Referência Multibanco gerada"),
            order = self
        )
        self.email_sent = True
        self.save()

    def email_mime(self):
        return "%s <%s>" % (self.s_billing_name, self.s_email)
