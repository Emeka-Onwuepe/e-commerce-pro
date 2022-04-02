const cartflex = document.getElementById("cartflex")
const grand_total = document.getElementById('grand_total')
const customerForm = document.forms.customerForm

// const csrtoken = document.getElementsByName("csrfmiddlewaretoken")[0].value


// div.innerHTML = data
const state = getState()
user_cart = state.user_cart
let Total = 0
for (const product of user_cart) {
    Total += product.productTotal
    let div = document.createElement("div")
    div.className = 'productDiv'
    div.id = product.Id
    let productData = `<p>${product.product_type}</p>
                        <p>Color: ${product.color}</p>
                        <p>Size: ${product.size}</p>
                        <p>Price: <span id="price;${product.Id}">  ${product.price}</span> </p>
                        <p>Qty: <span id="qty;${product.Id}"> ${product.qty} </span> </p>
                        <p>Total: <span id="total;${product.Id}"> ${product.productTotal}</span> </p>
                        <button class="increment" id="incremet;${product.Id}">+</button>
                        <button class="decrement" id="decrement;${product.Id}">-</button>
                        <button class="decrement" id="delete;${product.Id}">Delete</button>
                        `

    div.innerHTML = productData
    cartflex.appendChild(div)
}
grand_total.innerHTML = Total

const priceEvent = (e, action) => {
    const button = e.target
    const Id = button.id.split(";")[1]
    const total = document.getElementById(`total;${Id}`)
    const qty = document.getElementById(`qty;${Id}`)
    const price = document.getElementById(`price;${Id}`)

    // let Total = parseFloat(total.innerHTML.split(" ")[1])
    let Qty = parseInt(qty.innerHTML)
    let Price = parseFloat(price.innerHTML)
    if (action == "increment") {
        Qty++
        grand_total.innerHTML = Total + Price
    } else if (action == "decrement") {
        Qty--
        grand_total.innerHTML = Total - Price
    }
    if (Qty > 0) {
        qty.innerHTML = Qty
        total.innerHTML = Price * Qty
        if (action == "increment") {
            Total += Price
            grand_total.innerHTML = Total
        } else if (action == "decrement") {
            Total -= Price
            grand_total.innerHTML = Total
        }
        const previousCart = getState().user_cart
        previousCart.forEach(product => {
            if (product.Id == Id) {
                product.qty = Qty
                product.productTotal = product.price * Qty
            }
        });
        storestate = storeReducer(UpdateCart(previousCart, 'user_cart'))
        setState(storestate)
    }

}

const deleteItem = (e) => {
    const button = e.target
    const Id = button.id.split(";")[1]
    const div = document.getElementById(`${Id}`)
    const total = document.getElementById(`total;${Id}`)
    grand_total.innerHTML = Total - parseFloat(total.innerHTML)
    div.remove()
    const previousCart = getState().user_cart
    const filtered = previousCart.filter(item => item.Id != Id)
    storestate = storeReducer(UpdateCart(filtered, 'user_cart'))
    setState(storestate)
    setSalesCount(storestate.user_cart)
}


const setCustomerData = (data) => {
    customerForm.elements.name.value = data.name
    customerForm.elements.phone_number.value = data.phone_number
    customerForm.elements.email.value = data.email
    customerForm.elements.address.value = data.address
}

setCustomerData(state.customer)


const updateUserState = (e) => {
    let target = e.target
    let customer = getState().customer
    customer[target.name] = target.value
    let storestate = storeReducer(addCustomer(customer))
    setState(storestate)

}

// getOrder({ phone_number: getState().customer.phone_number })
//     .then(data => {
//         console.log(data)
//     })
//     .catch(error => alert(error))

customerForm.elements.name.addEventListener('change', updateUserState)
customerForm.elements.phone_number.addEventListener('change', updateUserState)
customerForm.elements.email.addEventListener('change', updateUserState)
customerForm.elements.address.addEventListener('change', updateUserState)

const incrementButtons = document.getElementsByClassName("increment")
for (const button of incrementButtons) {
    button.addEventListener('click', (e) => priceEvent(e, "increment"))
}
const decrementButtons = document.getElementsByClassName("decrement")
for (const button of decrementButtons) {
    button.addEventListener('click', (e) => priceEvent(e, "decrement"))
}
const deleteButtons = document.getElementsByClassName("delete")
for (const button of decrementButtons) {
    button.addEventListener('click', deleteItem)
}


// pay Stack integration

const public_key = document.getElementById("public_key").innerHTML
const make_payment_button = document.getElementById("make_payment")

function payWithPaystack() {

    const date = Date.now().toString().slice(5)
    const random = Math.floor(Math.random() * 100)
    const OrderId = `smb${random}${date}`

    const data = {
        action: "create",
        name: customerForm.elements.name.value,
        phone_number: customerForm.elements.phone_number.value,
        email: customerForm.elements.email.value,
        address: customerForm.elements.address.value,
        payment_method: 'online',
        remark: "Website Sales",
        total_amount: Total,
        expected_amount: Total,
        purchase_id: OrderId,
        orders: getState().user_cart
    }

    ProcessOrder(data, csrtoken, 'processorder').
    then(data => {
            storestate = storeReducer(clearCart("user_cart"))
            setState(storestate)
            setSalesCount(storestate.user_cart)

            const childNodes = cartflex.children
            for (const div of childNodes) {
                div.remove()
            }
            grand_total.innerHTML = 0
            Total = 0
        })
        .catch((error) => {
            alert(error)
            setState(storeReducer(load(LOADED)))
        });

    var handler = PaystackPop.setup({

        key: public_key, // Replace with your public key

        email: customerForm.elements.email.value,

        amount: Total * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit

        currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars

        ref: OrderId, // Replace with a reference you generated

        callback: function(response) {
            //this happens after the payment is completed successfully
            var reference = response.reference;
            alert('Payment complete! Reference: ' + reference);

            // Make an AJAX call to your server with the reference to verify the transaction
            const data = {
                action: "payment",
                purchase_id: OrderId,

            }
            ProcessOrder(data, csrtoken, 'processorder').
            then(data => {
                    // wait here
                })
                .catch((error) => {
                    alert(error)
                    setState(storeReducer(load(LOADED)))
                });
        },

        onClose: function() {

            alert('Transaction was not completed, window closed.');

        },

    });

    handler.openIframe();

    // if ()

}

make_payment_button.addEventListener('click', payWithPaystack)