#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

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

    VALID_PAYMENTS = (
        "Multibanco",
        "Ref. Multibanco"
    )

    MIN_VALUE = 0.5

    s_id = appier.field(
        type = int,
        index = True,
        immutable = True,
        default = True,
        description = "ID"
    )

    s_name = appier.field(
        index = True,
        immutable = True,
        description = "Name",
        observations = """The descriptive name/identifier
        of the order, to be human readable"""
    )

    s_total_price = appier.field(
        index = True,
        immutable = True,
        description = "Total Price",
        observations = """The total financial value of the
        order in the order defined currency"""
    )

    s_currency = appier.field(
        index = True,
        immutable = True,
        description = "Currency"
    )

    s_quantity = appier.field(
        type = int,
        index = True,
        immutable = True,
        description = "Quantity"
    )

    s_gateway = appier.field(
        index = True,
        immutable = True,
        description = "Gateway"
    )

    s_status = appier.field(
        index = True,
        immutable = True,
        description = "Status"
    )

    s_fulfillment = appier.field(
        index = True,
        immutable = True,
        description = "Fulfillment"
    )

    s_email = appier.field(
        index = True,
        immutable = True,
        meta = "email",
        description = "Email"
    )

    s_shipping_name = appier.field(
        index = True,
        immutable = True,
        description = "Shipping Name"
    )

    s_shipping_street = appier.field(
        index = True,
        immutable = True,
        description = "Shipping Street"
    )

    s_shipping_city = appier.field(
        index = True,
        immutable = True,
        description = "Shipping City"
    )

    s_shipping_province = appier.field(
        index = True,
        immutable = True,
        description = "Shipping Province"
    )

    s_shipping_country_code = appier.field(
        index = True,
        immutable = True,
        description = "Shipping Country Code"
    )

    s_shipping_zip = appier.field(
        index = True,
        immutable = True,
        description = "Shipping Zip Code"
    )

    s_billing_name = appier.field(
        index = True,
        immutable = True,
        description = "Billing Name"
    )

    payment = appier.field(
        type = int,
        safe = True,
        index = True,
        meta = "enum",
        enum = PAYMENT_S
    )

    note_sent = appier.field(
        type = bool,
        safe = True,
        index = True
    )

    email_sent = appier.field(
        type = bool,
        safe = True,
        index = True
    )

    warning_sent = appier.field(
        type = bool,
        safe = True,
        index = True
    )

    confirmation_sent = appier.field(
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

    reference_id = appier.field(
        index = True,
        description = "Reference ID"
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
    def list_names(cls):
        return [
            "s_name",
            "s_total_price",
            "s_gateway",
            "s_billing_name",
            "created",
            "payment"
        ]

    @classmethod
    def order_name(cls):
        return ("s_id", -1)

    @classmethod
    def from_shopify(cls, order, transactions = [], strict = False):
        gateway = order.get("gateway", None)
        line_items = order.get("line_items", [])
        shipping_address = order.get("shipping_address", {})
        billing_address = order.get("billing_address", {})
        quantity = sum([line_item["quantity"] for line_item in line_items])
        shipping_name = shipping_address.get("name", None)
        shipping_address1 = shipping_address.get("address1", None)
        shipping_address2 = shipping_address.get("address2", None)
        shipping_city = shipping_address.get("city", None)
        shipping_province = shipping_address.get("province", None)
        shipping_country_code = shipping_address.get("country_code", None)
        shipping_zip = shipping_address.get("zip", None)
        billing_name = billing_address.get("name", None)
        shipping_street = "%s%s" % (shipping_address1 or "", shipping_address2 or "")
        if transactions: gateway = transactions[0].get("gateway", gateway)
        if strict and not gateway:
            raise appier.OperationalError(
                message = "No gateway defined for order"
            )
        return cls(
            s_id = order["id"],
            s_name = order["name"],
            s_total_price = order["total_price"],
            s_currency = order["currency"],
            s_status = order["financial_status"],
            s_fulfillment = order["fulfillment_status"],
            s_email = order["email"],
            s_quantity = quantity,
            s_gateway = gateway,
            s_shipping_name = shipping_name,
            s_shipping_street = shipping_street,
            s_shipping_city = shipping_city,
            s_shipping_province = shipping_province,
            s_shipping_country_code = shipping_country_code,
            s_shipping_zip = shipping_zip,
            s_billing_name = billing_name,
            note_sent = False,
            email_sent = False,
            warning_sent = False
        )

    @classmethod
    @appier.link(name = "Generate MB")
    def generate_mb(cls, absolute = False):
        return appier.get_app().url_for(
            "order.generate_mb_json",
            absolute = absolute
        )

    @classmethod
    @appier.link(name = "Export Shelve")
    def export_shelve_url(cls, absolute = False):
        return appier.get_app().url_for(
            "admin.export_shelve",
            absolute = absolute
        )

    @classmethod
    @appier.link(name = "Export CTT", context = True)
    def ctt_csv_url(cls, view = None, context = None, absolute = False):
        return appier.get_app().url_for(
            "order.ctt_csv",
            view = view,
            context = context,
            absolute = absolute
        )

    @classmethod
    @appier.operation(
        name = "Import Shelve",
        parameters = (
            ("Shelve File", "file", "file"),
        )
    )
    def import_shelve_s(cls, file):
        _file_name, _mime_type, data = file
        app = appier.get_app()
        shelve_path = app.scheduler.easypay.path
        shelve_path = os.path.abspath(shelve_path)
        file = open(shelve_path, "wb")
        try: file.write(data)
        finally: file.close()

    @classmethod
    @appier.view(name = "Paid")
    def paid_v(cls, *args, **kwargs):
        kwargs["sort"] = kwargs.get("sort", [("s_id", -1)])
        kwargs.update(s_status = "paid")
        return appier.lazy_dict(
            model = cls,
            kwargs = kwargs,
            entities = appier.lazy(lambda: cls.find(*args, **kwargs)),
            page = appier.lazy(lambda: cls.paginate(*args, **kwargs))
        )

    def pre_validate(self):
        appier_extras.admin.Base.pre_validate(self)

        self.start_payment()

    def start_payment(self):
        if hasattr(self, "payment") and self.payment: return
        self.payment = Order.PAID
        if not hasattr(self, "s_status") or not self.s_status: return
        if not hasattr(self, "s_gateway") or not self.s_gateway: return
        if not self.s_gateway in Order.VALID_PAYMENTS: return
        if float(self.s_total_price) < Order.MIN_VALUE: return
        if self.s_status == "pending": self.payment = Order.PENDING; return
        if self.s_status == "refunded": self.payment = Order.REFUNDED; return

    def issue_reference_s(self, easypay):
        amount = float(self.s_total_price)
        reference = easypay.generate_mb(amount)
        self.entity = reference["entity"]
        self.reference = reference["reference"]
        self.reference_id = reference["identifier"]
        self.payment = Order.ISSUED
        self.save()
        self.logger.debug("Issued reference for order '%s'" % self.s_name)

    def pay_s(self, shopify, strict = True):
        try:
            shopify.pay_order(self.s_id)
        except Exception:
            self.logger.error("Problem confirming payment for order '%s'" % self.s_name)
            if strict: raise

        self.payment = Order.PAID
        self.save()
        self.logger.debug("Received payment for order '%s'" % self.s_name)

    def cancel_s(self, easypay, shopify, strict = True):
        try:
            easypay.cancel_mb(self.reference_id)
            shopify.cancel_order(self.s_id, email = True)
        except Exception:
            self.logger.error("Problem canceling order '%s'" % self.s_name)
            if strict: raise

        self.payment = Order.CANCELED
        self.save()
        self.logger.debug("Canceled and reversed order '%s'" % self.s_name)

    def note_reference_s(self, shopify):
        order = shopify.get_order(self.s_id)
        note = order.get("note", None) or ""
        note += "Entity: %s\nReference: %s\nValue: %s\n" % (
            self.entity, self.reference, self.s_total_price
        )
        shopify.update_order(self.s_id, note = note)
        self.note_sent = True
        self.save()

    def email_reference_s(self):
        self.send_email(
            "email/reference.html.tpl",
            receivers = [self.email_mime()],
            subject = self.to_locale("Dados para pagamento %s" % self.s_name),
            order = self
        )
        self.email_sent = True
        self.save()

    def email_warning_s(self):
        self.send_email(
            "email/warning.html.tpl",
            receivers = [self.email_mime()],
            subject = self.to_locale("Alerta para pagamento %s" % self.s_name),
            order = self
        )
        self.warning_sent = True
        self.save()

    def email_confirmation_s(self):
        self.send_email(
            "email/confirmation.html.tpl",
            receivers = [self.email_mime()],
            subject = self.to_locale("Confirmação de pagamento %s" % self.s_name),
            order = self
        )
        self.confirmation_sent = True
        self.save()

    def email_mime(self):
        return "%s <%s>" % (self.s_billing_name, self.s_email)

    @appier.operation(name = "Send reference email")
    def email_reference(self):
        self.email_reference_s()

    @appier.operation(name = "Send warning email")
    def email_warning(self):
        self.email_warning_s()

    @appier.operation(name = "Send confirmation email")
    def email_confirmation(self):
        self.email_confirmation_s()

    @appier.operation(name = "Mark confirmation sent")
    def mark_confirmation_sent(self):
        self.confirmation_sent = True
        self.save()
