frappe.ready(function(){
    $('#addToCart').on('click', function(){

        frappe.call({
            method: "accounting.accounting.doctype.item.item.add_to_cart",
            args: {
                "name": '{{ doc.name }}',
                "image": '{{ doc.image }}',
                "price":  '{{ doc.price }}',
                "route": '{{ doc.route }}',
                "quantity": $("#quantitySelector").val(),
            },
            callback: ()=>{
                frappe.msgprint(`Item added to Cart`)
            },
        })
    });
})