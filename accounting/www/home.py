import frappe

def get_context(context):
    context.items = frappe.get_all('Item', fields = ['image', 'item_name', 'price', 'description', 'route'])
    return context