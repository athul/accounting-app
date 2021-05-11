import frappe
from frappe.utils import nowdate
from frappe import get_print


def get_context(context):
    context.cart_items = frappe.get_all(
        'Shopping Cart', fields=['image', 'item_name', 'price', 'route', 'quantity'])
    context.sum = frappe.get_all('Shopping cart', fields=[
                                 'sum(price*quantity) as sum'])
    return context


@frappe.whitelist(allow_guest=True)
def remove_item_from_cart(name):
    frappe.delete_doc('Shopping Cart', name, ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def create_sales_invoice(user: str):
    try:
        frappe.get_doc("Person", user)
    except:
        create_customer(user)
    # parties = frappe.get_doc("Person",user)
    # print("*\n"*10,parties.as_dict(),"\n*"*10)
    # return parties.as_dict()
    # parties = frappe.get_doc("Person", user)
    cart_items = frappe.get_all("Shopping Cart", [
        '(item_name) as item', '(price) as rate', 'quantity', '(price*quantity) as total'])
    sales_invoice = frappe.get_doc({
        "doctype": "Sales Invoice",
        "title": f"Sales Invoice - {nowdate()}",
        "posting_date": nowdate(),
        "party": user,
        "items": cart_items,
        "total": sum([item['total'] for item in cart_items])
    })
    sales_invoice.insert(ignore_permissions=True)
    sales_invoice.submit()
    return sales_invoice.as_dict()


@frappe.whitelist(allow_guest=True)
def create_customer(name: str) -> str:
    party = frappe.get_doc({
        "doctype": "Person",
        "party_name": name,
        "type": "Customer"
    })
    party.insert(ignore_permissions=True)
    return party.party_name
