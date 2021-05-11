import frappe

def execute():
    sales_invoices = frappe.get_all("Sales Invoice")
    for invoice in sales_invoices:
        sls = frappe.get_doc("Sales Invoice",invoice.name)
        try:
            sls.save()
        except:
            frappe.log_error()