import frappe


def get_context(context):
    context.cart_items = frappe.get_all(
        'Shopping Cart', fields=['image', 'item_name', 'price', 'route','quantity'])
    context.sum = frappe.get_all('Shopping cart', fields=['sum(price*quantity) as sum'])
    return context


@frappe.whitelist(allow_guest=True)
def remove_item_from_cart(name):
    frappe.delete_doc('Shopping Cart', name)