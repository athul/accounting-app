# Copyright (c) 2013, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = getColumns(filters)
	data = getData(filters)
	return columns, data

def getColumns(filters=None):
	columns = [{
		"fieldname" : "posting_date",
		"label" : _("Posting Date"),
		"fieldtype" : "Date",
		"width" : 120
	},
	{
		"fieldname" : "account",
		"label" : _("Account"),
		"fieldtype" : "Link",
		"options" : "Account",
		"width" : 150
	},
	{
		"fieldname" : "debit_amount",
		"label" : _("Debit"),
		"fieldtype" : "Currency",
		"width" : 120
	},
	{
		"fieldname" : "credit_amount",
		"label" : _("Credit"),
		"fieldtype" : "Currency",
		"width" : 120
	},
	{
		"fieldname" : "transaction_type",
		"label" : _("Transaction Type"),
		"fieldtype" : "Select",
		"options" : "Purchase Invoice\nSales Invoice\nPayment Entry\nJournal Entry",
		"width" : 300
	},
	{
		"fieldname" : "transaction_number",
		"label" : _("Transaction Number"),
		"fieldtype" : "Dynamic Link",
		"options" : "transaction_type",
		"width" : 300
	}]

	return columns

def getData(filters):
	glEntries = frappe.get_list(
		"General Ledger",
		filters={
			"transaction_type":filters.get("transaction_type"),
			"transaction_number":filters.get("transaction_number")
		},
		fields=['posting_date','account', 'debit_amount', 'credit_amount', 'transaction_number', 'transaction_type']
	)
	return glEntries