# Copyright (c) 2013, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from typing import Dict, List
from frappe import _
import frappe
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
    columns = getColumns(filters)
    data = getData(filters)
    return columns, data


def getColumns(filters) -> List[Dict]:
    columns = [{
        "fieldname": "account",
        "label": _("Account"),
        "fieldtype": "Link",
        "options": "Account",
        "width": 300
    },
        {
        "fieldname": "balance",
        "label": _("Balance"),
        "fieldtype": "Currency",
        "width": 250
    }]
    return columns


def getData(filters) -> List:
    """Return as a List a assets and liabilities
    """
    data = []
    asset_accounts = get_descendants_of(
        "Account", "Application of Funds (Assets) - TB")
    liability_accounts = get_descendants_of(
        "Account", "Source of Funds (Liabilities) - TB")

    parent_assets = {
        "indent": 0,
        "account": "Application of Funds (Assets) - TB"
    }
    data.append(parent_assets)
    assets = frappe.get_all(
        "General Ledger", filters={
            "account": ["in", asset_accounts]
        }, fields=["account", "sum(credit_amount) as balance"],
        group_by="account"
    )
    for asset in assets:
        report_entry = {
            "indent": 1,
            "account": asset.account,
            "balance": asset.balance,
            "parent_account": parent_assets['account']
        }
        data.append(report_entry)
    parent_liabilities = {
        'indent': 0,
        'account': "Source of Funds (Liabilities) - TB"
    }
    data.append(parent_liabilities)
    liabilities = frappe.get_all(
        "General Ledger",
        filters={
            "account": ["in", liability_accounts]
        },
        fields=["account", 'sum(debit_amount) as balance'],
        group_by="account"
    )
    for lblt in liabilities:
        report_entry = {
            "indent": 1,
            "account": lblt.account,
            "balance": lblt.balance,
            "parent_account": parent_liabilities['account']
        }
        data.append(report_entry)
    return data
