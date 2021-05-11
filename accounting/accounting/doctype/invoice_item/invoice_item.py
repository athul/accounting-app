# -*- coding: utf-8 -*-
# Copyright (c) 2021, Athul Cyriac Ajay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class InvoiceItem(Document):
	def before_save(self):
		self.total = self.rate * self.quantity
