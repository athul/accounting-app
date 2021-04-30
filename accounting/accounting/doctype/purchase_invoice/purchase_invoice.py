# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
    def before_save(self):
        self.calc_amount()

    def calc_amount(self):
        total = 0
        for item in self.get("items"):
            total += item.quantity * item.rate
        self.total_amount = total

    def on_submit(self):
        self.new_gl_entry()

    def new_gl_entry(self):
        debGlEntry = frappe.get_doc({
            "doctype": "General Ledger",
            "posting_date": self.posting_date,
            "debit_amount": self.total_amount,
            "credit_amount": 0,
            "account": "Creditors",
            "transaction_type": "Purchase Invoice",
            "transaction_number": self.name
        })
        credGlEntry = frappe.get_doc({
            "doctype": "General Ledger",
            "posting_date": self.posting_date,
            "debit_amount": 0,
            "credit_amount": self.total_amount,
            "account": "Expenses",
            "transaction_type": "Purchase Invoice",
            "transaction_number": self.name,
        })
        debGlEntry.insert()
        credGlEntry.insert()
