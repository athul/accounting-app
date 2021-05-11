# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


class TestSalesInvoice(unittest.TestCase):
    def tearDown(self) -> None:
        frappe.db.rollback()

    def test_ledger_entry(self):
        before_sales_count = frappe.db.count("General Ledger")
        doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "title": "OP Phones",
            "posting_date": "2020-05-10",
            "items": [{
                "item": "OnePlus Nord",
                "quantity": 2,
                "rate":29000
            },
            {
                "item": "Silicon",
                "quantity": 2,
                "rate":200
            }],
            "party":"Jim"
        })
        doc.insert()
        doc.submit()
        after_sales_count = frappe.db.count("General Ledger")
        diff = after_sales_count - before_sales_count
        self.assertEqual(
            diff, 2, "No two Ledger Entries are to be created on a Sales Invoice")
