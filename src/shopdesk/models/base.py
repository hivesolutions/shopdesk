#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier
import shopify
import appier_extras


class ShopdeskBase(appier_extras.admin.Base):

    @classmethod
    def is_abstract(cls):
        return True

    @property
    def shopify_api(self):
        return shopify.API(
            api_key=appier.conf("SHOPIFY_API_KEY"),
            password=appier.conf("SHOPIFY_PASSWORD"),
            secret=appier.conf("SHOPIFY_SECRET"),
            store_url=appier.conf("SHOPIFY_STORE"),
        )
