#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import appier_extras

class Order(appier_extras.admin.Base):

    PENDING = 1
    ISSUED = 2
    PAID = 3
    REFUNDED = 4
    OTHER = 5

    PAYMENT_S = {
        PENDING : "pending",
        ISSUED : "issued",
        PAID : "paid",
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

    s_gateway = appier.field(
        index = True,
        immutable = True
    )

    s_status = appier.field(
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
