# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator


class Item(WebsiteGenerator):
    pass


@frappe.whitelist(allow_guest=True)
def add_to_cart(name, image, price, route, quantity):
    cart_item = frappe.get_doc({
        "doctype": "Shopping Cart",
        "item_name": name,
        "price": price,
        "image": image,
        "route": route,
        "quantity": quantity
    })
    cart_item.insert()
