from typing import List, Union
import frappe


def calculate_total(items: List) -> float:
    """ Calculate the Total Amount of Items
    """
    total = 0
    for item in items:
        total += item.quantity * item.rate
    return total


def new_gl_entry(total: str, posting_date: str, name: str, purchase: bool = False):
    """ 
        - Inserts a row to General Ledger on a New Sales Invoice.
        - Inserts total amount as debit to the Sales account
        - Inserts total amount as credit to Debitors account
    """
    if purchase:
        debit_account = "Creditors"
        credit_account = "Expenses"
        transaction_type = "Purchase Invoice"
    else:
        debit_account = "Sales"
        credit_account = "Debtors"
        transaction_type = "Sales Invoice"

    debit_gl_entry = frappe.get_doc({
        "doctype": "General Ledger",
        "posting_date": posting_date,
        "debit_amount": total,
        "credit_amount": 0,
        "account": debit_account,
        "transaction_type": transaction_type,
        "transaction_number": name
    })
    credit_gl_entry = frappe.get_doc({
        "doctype": "General Ledger",
        "posting_date": posting_date,
        "debit_amount": 0,
        "credit_amount": total,
        "account": credit_account,
        "transaction_type": transaction_type,
        "transaction_number": name,
    })
    debit_gl_entry.insert()
    credit_gl_entry.insert()
