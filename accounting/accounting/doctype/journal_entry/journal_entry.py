# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class JournalEntry(Document):
    def validate(self):
        self.validate_credit_debit_sum()

    def validate_credit_debit_sum(self):
        """Checks if the Entry is Balanced"""
        self.total_credit, self.total_debit = 0, 0
        for account in self.get("accounts"):
            self.total_credit += account.credit
            self.total_debit += account.debit
        if self.total_credit != self.total_debit:
            frappe.throw(_('Total credit should be equal to total debit.'))

    def on_submit(self):
        self.enter_gl()

    def enter_gl(self, rev: bool = False):
        """ Inserts a Row into General Ledger when a Journal Entry is submitted
        """
        for account in self.get("accounts"):
            newGlEntry = frappe.get_doc({
                "doctype": "General Ledger",
                "posting_date": self.posting_date,
                "account": account.account,
                "debit_amount": account.debit if not rev else account.credit,
                "credit_amount": account.credit if not rev else account.debit,
                "transaction_type": "Journal Entry",
                "transaction_number": self.name,
            })
            newGlEntry.insert()

    def on_cancel(self):
        self.enter_gl(True)
