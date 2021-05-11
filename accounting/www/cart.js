function deleteFromCart(item) {
  frappe.call({
    method: "accounting.www.cart.remove_item_from_cart",
    args: {
      name: item,
    },
    callback: () => {
      frappe.msgprint(__(`${item} removed!`));
      setTimeout(function () {
        window.location.href = "/cart";
      }, 2000);
    },
    error: () => {
      frappe.msgprint({
        title: `Error Removing Item`,
        indicator: "red",
      });
    },
  });
}
// If you're using the code for reference,
// maybe delete the items of the cart after a sales invoice
// has been generated
var generateSalesInvoice = () => {
  var customerName = $("#customerName").val();
  if (customerName == undefined) {
    customerName = "Jim";
  }
  console.log(customerName);
  frappe.call({
    method: "accounting.www.cart.create_sales_invoice",
    args: {
      user: customerName,
    },
    callback: (r) => {
      console.log(r)
      var link = `http://accounting:8000/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name=${r.message.name}&format=Sales%20Invoice%20Format&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en`;
      frappe.msgprint({
        title: `Sales Invoice Generated`,
        message: "Redirecting to Generated Invoice in 2 seconds",
        indicator: "Green",
      });
      setTimeout(() => {
        window.location.href = link;
      }, 2000);
    },
  });
};
