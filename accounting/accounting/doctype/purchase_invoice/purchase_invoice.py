# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from accounting.accounting.doctype.transactions import calculate_total, new_gl_entry
#import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
    def before_save(self):
        self.total = calculate_total(self.get("items"))

    def on_submit(self):
        new_gl_entry(total=self.total, posting_date=self.posting_date,
                     name=self.name, purchase=True)
