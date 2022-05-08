const cartflex = document.getElementById("cartflex")
const grand_total = document.getElementById('grand_total')
const total_node = document.getElementById('total')
const ltotal = document.getElementById('ltotal')
const customerForm = document.forms.customerForm
let tbody = document.querySelector("#tbody")
const emptycart = document.querySelector(".emptycart")
const logistics = document.getElementById("logistics")
    // const amounts = document.querySelectorAll(".amount")

// const csrtoken = document.getElementsByName("csrfmiddlewaretoken")[0].value


// div.innerHTML = data
const state = getState()
user_cart = state.user_cart
let Total = 0
let previousLog = 0
for (const product of user_cart) {
    Total += product.productTotal
    let div = document.createElement("div")
    div.className = 'productDiv'
    div.id = product.Id
    let productData = `<h3>${product.product_type}</h3>
                        <p>Color: ${product.color}</p>
                        <p>Size: ${product.size}</p>
                        <p>Price:  &#8358 <span class="amount" id="price;${product.Id}">${product.price}</span></p>
                        <p>Qty: <span  id="qty;${product.Id}"> ${product.qty} </span> </p>
                        <p><strong>Total:  &#8358 <span class="amount" id="total;${product.Id}">${product.productTotal}</span></strong></p>
                        <button class="increment" id="incremet;${product.Id}">+</button>
                        <button class="decrement" id="decrement;${product.Id}">-</button>
                        <button class="delete" id="delete;${product.Id}">Delete</button>
                        `

    div.innerHTML = productData
    cartflex.appendChild(div)
}
grand_total.innerHTML = addComas(Total.toString())

const handleEmptycartPara = () => {
    if (Total == 0) {
        emptycart.style.display = "block"
    } else {
        emptycart.style.display = "none"
    }
}
handleEmptycartPara()

const manageCustomerDetails = (e, display) => {
    const customerDetails = document.querySelector("#customerDetails")
    if (display) {
        customerDetails.style.display = 'block'
        e.target.style.display = "none"
    } else {
        customerDetails.style.display = 'none'
    }
}
const manageProcessOrderButton = () => {
    const process_order = document.getElementById("process_order")
    if (Total > 0) {
        process_order.style.display = 'block'
        process_order.style.marginBottom = '30px'
        process_order.addEventListener('click', (e) => manageCustomerDetails(e, true))
    } else {
        process_order.style.display = "none"
    }
}
manageProcessOrderButton()

const priceEvent = (e, action) => {
    const button = e.target
    const Id = button.id.split(";")[1]
    const total = document.getElementById(`total;${Id}`)
    const qty = document.getElementById(`qty;${Id}`)
    const price = document.getElementById(`price;${Id}`)
        // let Total = convertToFloat(total.innerHTML.split(" ")[1])
    let Qty = parseInt(qty.innerHTML)
    let Price = convertToFloat(price.innerHTML)
    if (action == "increment") {
        Qty++
        //grand_total.innerHTML = Total + Price
    } else if (action == "decrement") {
        Qty--
        //grand_total.innerHTML = Total - Price
    }
    if (Qty > 0) {
        qty.innerHTML = Qty
        let input = Price * Qty
        total.innerHTML = addComas(input.toString())
        if (action == "increment") {
            Total += Price
            grand_total.innerHTML = addComas(Total.toString())
        } else if (action == "decrement") {
            Total -= Price
            grand_total.innerHTML = addComas(Total.toString())
        }
        const previousCart = getState().user_cart
        previousCart.forEach(product => {
            if (product.Id == Id) {
                product.qty = Qty
                product.productTotal = product.price * Qty
            }
        });
        manageProcessOrderButton()
        storestate = storeReducer(UpdateCart(previousCart, 'user_cart'))
        setState(storestate)
    }

}


const addLogistics = () => {
    Total = (Total - previousLog) + parseFloat(logistics.value)
    grand_total.innerHTML = addComas(Total.toString())
    previousLog = parseFloat(logistics.value)
    if (previousLog > 0) {
        total_node.innerHTML = addComas((Total - previousLog).toString())
        total_node.parentNode.parentNode.style.display = "block"
        ltotal.innerHTML = addComas(previousLog.toString())
        ltotal.parentNode.parentNode.style.display = "block"
    } else {
        total_node.parentNode.parentNode.style.display = "none"
        ltotal.parentNode.parentNode.style.display = "none"
    }
}

addLogistics()
logistics.addEventListener('change', addLogistics)

const resetcart = () => {
    Total = 0
    previousLog = 0
    logistics.value = 0
    grand_total.innerHTML = 0
    total_node.innerHTML = 0
    ltotal.innerHTML = 0
    total_node.parentNode.parentNode.style.display = "none"
    ltotal.parentNode.parentNode.style.display = "none"
    customerDetails.style.display = 'none'
}

const Confirm = (Id) => {
    const confirmBox = document.getElementById('confirmBox')
    const confirmDelete = document.querySelector(".confirmDelete")
    confirmDelete.id = Id + ";none"
    let x_axis = document.documentElement.clientWidth ||
        document.body.clientWidth;
    if (x_axis >= 1000) {
        let num = (x_axis - 780) / 2
        confirmBox.style.marginLeft = `${num}px`
    } else {
        let num = (x_axis - 332) / 2
        confirmBox.style.marginLeft = `${num}px`
    }
    confirmBox.style.display = 'block'
}

const handleCancelDelete = (e) => {
    e.preventDefault()
    const confirmBox = document.getElementById('confirmBox')
    confirmBox.style.display = 'none'

}

const handleConfirmDelete = (e) => {
    e.preventDefault()
    const Id = e.target.id.split(";")[0]
    const div = document.getElementById(`${Id}`)
    const total = document.getElementById(`total;${Id}`)
    grand_total.innerHTML = addComas((Total - convertToFloat(total.innerHTML)).toString())
    Total -= convertToFloat(total.innerHTML)
    manageProcessOrderButton()
    div.remove()
    if (cartflex.children.length == 0) {
        resetcart()
    }

    handleEmptycartPara()
    const confirmBox = document.getElementById('confirmBox')
    confirmBox.style.display = 'none'
    const previousCart = getState().user_cart
    const filtered = previousCart.filter(item => item.Id != Id)
    storestate = storeReducer(UpdateCart(filtered, 'user_cart'))
    setState(storestate)
    setSalesCount(storestate.user_cart)

}

const deleteItem = (e) => {
    const button = e.target
    const Id = button.id.split(";")[1]
    Confirm(Id)
}

try {
    const confirmDelete = document.querySelector('.confirmDelete')
    const cancelDelete = document.querySelector(".cancelDelete")
    confirmDelete.addEventListener("click", (e) => handleConfirmDelete(e))
    cancelDelete.addEventListener('click', (e) => handleCancelDelete(e))
} catch (error) {

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
    showOrderHistoryButton(storestate.customer.phone_number)

}

// getOrder({ phone_number: getState().customer.phone_number })
//     .then(data => {
//         console.log(data)
//     })
//     .catch(error => Alert(error))

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
for (const button of deleteButtons) {
    button.addEventListener('click', deleteItem)
}


for (const node of amounts) {
    node.innerHTML = addComas(node.innerHTML)
}


// pay Stack integration

const public_key = document.getElementById("public_key").innerHTML
const make_payment_button = document.getElementById("make_payment")



var contactInputs = document.querySelectorAll(".contactInput")
let errorMessages = {
    "name": "Only alphabets are allowed",
    "email": "Invalid email",
    "address": "Character not allowed",
    "phone_number": "Invalid phone number"
}

let errorTest = {
    "name": /[^a-z\s]/i,
    "email": /^[a-z]+\d*[a-z]*@[a-z]+\.\w+\s*$/gi,
    "address": /[^a-z\s.,;':@&)(0-9"#_-]/i,
    "phone_number": /[^0-9+\s]/i
}

const checkerror = (e, elem = undefined) => {
    let contactInput = elem ? elem : e.target
    let fieldName = contactInput.name;
    let fieldValue = contactInput.value;
    let fieldLength = fieldValue.length
    let selector = `${fieldName}er`;
    let errP = document.querySelector(`#${selector}`);
    errP.innerHTML = '';
    if (fieldName != "email" && errorTest[fieldName].test(fieldValue)) {
        errP.innerHTML = errorMessages[fieldName];
        contactInput.style.marginBottom = "0px";
    } else if (fieldName == "phone_number" && fieldLength < 11) {
        errP.innerHTML = errorMessages[fieldName];
        contactInput.style.marginBottom = "0px";

    } else if (fieldName == "email" && !errorTest[fieldName].test(fieldValue)) {
        errP.innerHTML = errorMessages[fieldName];
        contactInput.style.marginBottom = "0px";

    } else {
        errP.innerHTML = "";
        contactInput.style.marginBottom = "15px";
    }

    errP.style.color = 'red'
    errP.style.fontSize = '16px'

    if (fieldValue.length == 0) {
        errP.innerHTML = "";
        contactInput.style.marginBottom = "15px";
    }

    enableSubmitButton();

}

for (const contactInput of contactInputs) {
    checkerror(undefined, contactInput)
    contactInput.addEventListener("keyup", (e) => checkerror(e))
    contactInput.addEventListener("change", (e) => checkerror(e))

}


function enableSubmitButton() {
    let make_paymentbtn = document.getElementById("make_payment");
    for (const contactInput of contactInputs) {
        let fieldName = contactInput.name;
        let fieldLength = contactInput.value.length
        let selector = `${fieldName}er`;
        let errP = document.querySelector(`#${selector}`);
        if (fieldLength <= 0) {
            make_paymentbtn.disabled = true
            make_paymentbtn.style.backgroundColor = "gray";
            errP.innerHTML = fieldName + " must not be empty"
            errP.style.color = 'red'
            errP.style.fontSize = '16px'
            break;
        } else if (errP.innerHTML.length > 0) {
            make_paymentbtn.disabled = true
            make_paymentbtn.style.backgroundColor = "gray";
            break;
        } else {
            make_paymentbtn.disabled = false;
            make_paymentbtn.style.backgroundColor = "#0089A6";
            make_paymentbtn.style.color = "#ffffff";
        }

    }

}


function payWithPaystack() {

    loaderContainer.style.display = 'block'
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
        total_amount: Total - previousLog,
        expected_amount: Total - previousLog,
        logistics: previousLog,
        purchase_id: OrderId,
        orders: getState().user_cart
    }
    console.log(data)
    ProcessOrder(data, csrtoken, 'processorder').
    then(data => {
            storestate = storeReducer(clearCart("user_cart"))
            setState(storestate)
            setSalesCount(storestate.user_cart)

            // const childNodes = cartflex.children
            // for (const div of childNodes) {
            //     div.remove()
            // }
            cartflex.innerHTML = ""
            resetcart()
                // grand_total.innerHTML = 0
                // Total = 0
            handleEmptycartPara()
            manageCustomerDetails(undefined, false)
        })
        .catch((error) => {
            loaderContainer.style.display = 'none'
            Alert(error)
            setState(storeReducer(load(LOADED)))
        });

    try {
        var handler = PaystackPop.setup({

            key: public_key, // Replace with your public key

            email: customerForm.elements.email.value,

            amount: Total * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit

            currency: 'NGN', // Use GHS for Ghana Cedis or USD for US Dollars

            ref: OrderId, // Replace with a reference you generated

            callback: function(response) {
                //this happens after the payment is completed successfully
                var reference = response.reference;
                // Alert('Payment complete! Reference: ' + reference);

                // Make an AJAX call to your server with the reference to verify the transaction
                const data = {
                    action: "payment",
                    purchase_id: OrderId,

                }
                ProcessOrder(data, csrtoken, 'processorder').
                then(data => {
                        // wait here
                        loaderContainer.style.display = 'none'
                        Alert("Payment Completed ")

                    })
                    .catch((error) => {
                        loaderContainer.style.display = 'none'
                        Alert(error)
                        setState(storeReducer(load(LOADED)))
                    });
            },

            onClose: function() {
                loaderContainer.style.display = 'none'
                Alert('Transaction was not completed, window closed.');

            },

        });

        handler.openIframe();
    } catch (error) {
        error.name == 'ReferenceError' ? Alert("Your are offline," +
            " please go to your order history page to complete your order") : Alert(error)
        loaderContainer.style.display = 'none'
    }

    // if ()

}

make_payment_button.addEventListener('click', payWithPaystack)