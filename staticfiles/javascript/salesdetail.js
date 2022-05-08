const public_key = document.getElementById("public_key").innerHTML
const make_payment_button = document.getElementsByClassName("make_payment")

function payWithPaystack(e) {
    loaderContainer.style.display = 'block'
    const id = e.target.id
    const order_data = document.getElementById(`data${id}`)
    console.log(order_data.innerHTML.split(";"))
    const [OrderId, Total, email] = order_data.innerHTML.split(";")

    var handler = PaystackPop.setup({
        key: public_key, // Replace with your public key

        email: email,

        amount: parseFloat(Total) * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit

        currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars

        ref: OrderId, // Replace with a reference you generated

        callback: function(response) {
            //this happens after the payment is completed successfully
            var reference = response.reference;


            // Make an AJAX call to your server with the reference to verify the transaction
            const data = {
                action: "payment",
                purchase_id: OrderId,

            }
            ProcessOrder(data, csrtoken, 'processorder').
            then(data => {
                    // wait here
                    loaderContainer.style.display = 'none'
                    alert('Payment complete!');
                    const parentNode = e.target.parentNode
                    const paragraph = document.createElement("p")
                    paragraph.innerHTML = "Paid"
                    parentNode.appendChild(paragraph)
                    e.target.remove()

                })
                .catch((error) => {
                    loaderContainer.style.display = 'none'
                    alert(error)
                    setState(storeReducer(load(LOADED)))
                });
        },

        onClose: function() {
            loaderContainer.style.display = 'none'
            alert('Transaction was not completed, window closed.');

        },

    });

    handler.openIframe();

    // if ()

}

for (const button of make_payment_button) {
    button.addEventListener('click', payWithPaystack)
}