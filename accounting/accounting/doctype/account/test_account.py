# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


class TestAccount(unittest.TestCase):
    def test_account_create(self):
        if not frappe.db.exists("Account", "_Test Base Account"):
            createAccount("_Test Base Account", "112358", "Expenses", "Expense")

        acc_num, acc_name = frappe.db.get_value("Account", "_Test Base Account", [
                "account_number", "account_name"])
        self.assertEqual(acc_name, "_Test Base Account")
        self.assertEqual(acc_num, "112358")
        deleteAccount("_Test Base Account")


def createAccount(acc_name: str, acc_num: str, parent_acc: str, type: str):
    if not frappe.db.exists("Accounts", acc_name):
        doc = frappe.get_doc({
            "doctype": "Account",
            "account_name": acc_name,
            "account_number": acc_num,
            "parent_account": parent_acc,
            "root_type": type,
        })
        doc.insert()

def deleteAccount(name:str):
	frappe.delete_doc("Account", name)