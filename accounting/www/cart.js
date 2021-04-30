function deleteFromCart(item) {
  frappe.call({
    method: "accounting.www.cart.remove_item_from_cart",
    args: {
      name: item,
    },
    callback:()=>{
      frappe.msgprint(__(`${item} removed!`));
      setTimeout(function(){window.location.href = "/cart"} , 2000);
    },
    error: ()=>{
      frappe.msgprint({
        title:`Error Removing Item`,
        indicator:'red'
      })
    },
  },
  );
}
