# Copyright (c) 2013, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from typing import List
from frappe import _
import frappe
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
    columns = getColumns(filters)
    data = getData(filters)
    return columns, data


def getColumns(filters=None) -> List:
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


def getData(filters=None) -> List:
    data = []
    income, expense = 0, 0
    expense_accounts = get_descendants_of("Account", "Expenses")
    expense_accounts.append("Expenses")
    income_accounts = get_descendants_of("Account", "Income - TB")
    income_accounts.append("Income")
    parent_incomes = {
            "indent": 0,
            "account": "Income - TB"
        }
    data.append(parent_incomes)
    incomes = frappe.get_all(
        "General Ledger",
        filters={
            "account": ["in", income_accounts]
        },
        fields=["account", 'sum(debit_amount) as balance'],
        group_by="account"
    )
    for inc in incomes:
        report_entry = {
            "indent": 1,
            "account": inc.account,
            "balance": inc.balance,
            "parent_account": parent_incomes['account']
        }
        data.append(report_entry)
        income += inc.balance

    parent_expenses = {
        'indent': 0,
        'account': "Expenses"
    }
    data.append(parent_expenses)
    expenses = frappe.get_all(
        "General Ledger", filters={
            "account": ["in", expense_accounts]
        }, fields=["account", "sum(credit_amount) as balance"],
        group_by="account"
    )
    for expns in expenses:
        report_entry = {
            "indent": 1,
            "account": expns.account,
            "balance": -(expns.balance),
            "parent_account": parent_expenses['account']
        }
        data.append(report_entry)
        expense += expns.balance
    
    if income > expense:
        profit = income - expense
        data.append({'account': "Net Profit", 'balance': profit})
    else:
        loss = expense - income
        data.append({'account': "Net Loss", 'balance': loss})

    return data