let tbody = document.querySelector("#tbody")
const grandtotal = document.getElementById('grandtotal')
const expectedGroundTotal = document.getElementById('expectedgroundtotal')
const salesForm = document.forms.salesForm
const csrtoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
const userPhoneNumber = document.getElementById("user_phone_number")
const loaderContainer = document.getElementById("loaderContainer")

const setCustomerData = (data) => {
    salesForm.elements.name.value = data.name
    salesForm.elements.phone_number.value = data.phone_number
    salesForm.elements.email.value = data.email
    salesForm.elements.address.value = data.address
}


const setNumbering = () => {
    const sn = document.getElementsByClassName("sn")
    let num = 1
    for (const td of sn) {
        td.innerHTML = num++
    }
}

try {
    setNumbering()
} catch (error) {

}

const getCustomer = () => {
    loaderContainer.style.display = 'block'
    GetCustomer({ phone_number: userPhoneNumber.value }, csrtoken)
        .then(data => {
            let storestate = storeReducer(addCustomer(data.data))
            setState(storestate)
            setCustomerData(data.data)
            loaderContainer.style.display = 'none'
        })
        .catch(error => {
            loaderContainer.style.display = 'none'
            alert(error)
        })
}

const PriceEvent = (e) => {
    const Id = e.target.id.split("-")[0]
    const price = document.getElementById(`${Id}-price`)
    const qty = document.getElementById(`${Id}-qty`)
    const miniPrice = document.getElementById(`${Id}-miniPrice`)
    const expectedPrice = document.getElementById(`${Id}-expectedPrice`)
    const productTotal = document.getElementById(`${Id}-productTotal`)

    const product_total = convertToFloat(price.value) * parseFloat(qty.value)
    const expected_price = convertToFloat(miniPrice.innerHTML) * parseFloat(qty.value)
        // const grandtotal = document.getElementById('grandtotal')
    productTotal.innerHTML = addComas(product_total.toString())
    expectedPrice.innerHTML = addComas(expected_price.toString())

    const previousCart = getState().cart
    let total = 0
    let expectedTotal = 0
    previousCart.forEach(item => {
        if (item.Id == Id) {
            item.price = price.value;
            item.qty = qty.value;
            item.productTotal = product_total;
            item.expected = expected_price;
        }
        total += item.productTotal
        expectedTotal += item.expected
    })
    grandtotal.innerHTML = addComas(total.toString())
    expectedGroundTotal.innerHTML = addComas(expectedTotal.toString())
    storestate = storeReducer(UpdateCart(previousCart))
    setState(storestate)

}

const deleteEvent = (e) => {
    let target = e.target
    const Id = target.id.split("-")[0]
    const previousCart = getState().cart
    const productTotal = document.getElementById(`${Id}-productTotal`).innerHTML
    const expectedPrice = document.getElementById(`${Id}-expectedPrice`).innerHTML
    let parentNode = target.parentNode.parentNode
    grandtotal.innerHTML = addComas((convertToFloat(grandtotal.innerHTML) - convertToFloat(productTotal)).toString())
    expectedGroundTotal.innerHTML = addComas((convertToFloat(expectedGroundTotal.innerHTML) - convertToFloat(expectedPrice)).toString())
    parentNode.remove()
    setNumbering()
    const filtered = previousCart.filter(item => item.Id != Id)
    storestate = storeReducer(UpdateCart(filtered))
    setState(storestate)
}


const addPriceEvent = () => {
    const priceInput = document.getElementsByName("price")
    priceInput.forEach(div => {
        div.addEventListener("keyup", PriceEvent)
    })
    const qtyInput = document.getElementsByName("qty")
    qtyInput.forEach(div => {
        div.addEventListener("keyup", PriceEvent)
    })
    const deleteButtons = document.querySelectorAll(".delete")
    deleteButtons.forEach(div => {
        div.addEventListener("click", deleteEvent)
    })
}

let expanded = false;

function showCheckboxes(e) {
    let id = e.target.parentNode.id.split(';')[0]
    let checkboxes = document.getElementById(`${id}checkboxes`);
    if (!expanded) {
        checkboxes.style.display = "block";
        expanded = true;
    } else {
        checkboxes.style.display = "none";
        expanded = false;
    }
}


const addOrder = (e) => {
    e.preventDefault();
    let id = e.target.id
    let productList = []
    let data = document.getElementById(`${id}productData`).innerHTML
    let list = data.toString().split(";")

    if (list.length < 5) {
        let [id, product_type, color, image] = list
        let checkbox = document.getElementsByName(`${id}checkbox`)
        let selected = document.getElementById(`${id}checkboxes`)
        let selectionFound = false
        checkbox.forEach(node => {
            if (node.checked) {
                let product = {}
                let [Id, price, size] = node.dataset['data'].toString().split(";")
                selectionFound = true
                product.size = size
                product.id = parseInt(id)
                product.product_type = product_type
                product.image = image
                product.color = color
                product.price = parseFloat(price)
                product.mini = parseFloat(price)
                product.Id = `${product.id}_${Id}`
                product.qty = 1
                product.qty = 1
                product.productTotal = parseFloat(price)
                product.expected = parseFloat(price)
                productList.push(product)
                node.checked = false
            }
        })

        selected.style.display = "none";
        expanded = false;
        if (!selectionFound) {
            alert("No selection made, please make a selection.")
        }
    } else {
        let product = {}
        let [id, product_type, size, price, color, image] = list
        product.size = size
        product.price = parseFloat(price)
        product.mini = parseFloat(price)
        product.id = parseInt(id)
        product.Id = parseInt(id)
        product.product_type = product_type
        product.color = color
        product.image = image
        product.qty = 1
        product.productTotal = parseFloat(price)
        product.expected = parseFloat(price)
        productList.push(product)
    }

    // console.log(productList)
    const previousCart = getState().cart
    let purelist = []
    if (previousCart.length > 0) {
        productList.forEach(product => {
            const check = previousCart.filter(item => item.Id == product.Id)
            if (check.length == 0) {
                purelist.push(product)
            } else {
                alert(`${product.product_type} ${product.color} ${product.size} already added `)
            }
        });
    } else {
        purelist = productList;
    }


    // UpdateCart
    if (purelist.length > 0) {
        storestate = storeReducer(addToCart(purelist))
        setState(storestate)
            //const currentCart = getState().cart
            // setSalesCount(currentCart)
        appendOrderList(purelist)
        setNumbering()

        // handleDecisionBox()
    }

}


const manageLastSale = (data = null) => {
    const lastSale = document.getElementById("lastSale")
    const latestOrder = data ? data : getState().latestOrder
    if (latestOrder.purchase_id != "") {
        lastSale.lastChild.href = `/sales/sale/${latestOrder.purchase_id}/${latestOrder.type}`
    }

}
manageLastSale()



const processOrder = (e) => {
    loaderContainer.style.display = 'block'
    e.preventDefault()
    const date = Date.now().toString().slice(5)
    const random = Math.floor(Math.random() * 100)
    const OrderId = `smb${random}${date}`
    const data = {
        name: salesForm.elements.name.value,
        phone_number: salesForm.elements.phone_number.value,
        email: salesForm.elements.email.value,
        address: salesForm.elements.address.value,
        payment_method: salesForm.elements.payment_method.value,
        remark: salesForm.elements.remark.value,
        total_amount: convertToFloat(grandtotal.innerHTML),
        expected_amount: convertToFloat(expectedGroundTotal.innerHTML),
        purchase_id: OrderId,
        orders: getState().cart
    }
    if (data.orders.length > 0) {
        let verified = data.total_amount >= data.expected_amount ? true : false
        if (!verified) {
            verified = confirm("You are selling below the expected price." +
                " Are you sure you want to go ahead with this transaction?")
        }
        if (verified) {
            ProcessOrder(data, csrtoken).then(data => {
                    setState(storeReducer(addLatestOrder(data)))
                    manageLastSale(data)
                        // let rows = tbody.children
                    grandtotal.innerHTML = ""
                    salesForm.elements.name.value = ""
                    salesForm.elements.phone_number.value = ""
                    salesForm.elements.email.value = ""
                    salesForm.elements.address.value = ""
                    salesForm.elements.payment_method.value = ""
                    salesForm.elements.remark.value = ""
                    grandtotal.innerHTML = 0
                    expectedGroundTotal.innerHTML = 0

                    // let new_tbody = document.createElement("tbody")
                    // new_tbody.id = 'tbody'
                    tbody.innerHTML = ""
                    loaderContainer.style.display = 'none'
                })
                .catch((error) => {
                    loaderContainer.style.display = 'none'
                    alert(error)
                    setState(storeReducer(load(LOADED)))
                });
        } else {
            loaderContainer.style.display = 'none'

        }
    } else {
        loaderContainer.style.display = 'none'
        alert("No product selected")
    }

    // console.log(JSON.stringify(data))
}
const appendOrderList = (data) => {
    let total = convertToFloat(grandtotal.innerHTML)
    let expectTotal = convertToFloat(expectedGroundTotal.innerHTML)
    for (let i = 0; i < data.length; i++) {
        total += data[i].productTotal
        expectTotal += data[i].expected
        let newrow = tbody.insertRow()
        let tds = ` <td class="sn"></td>
        <td>${data[i].product_type}</td>
        <td>${data[i].color}</td>
        <td>${data[i].size}</td>
        <td><input type="text" name="price" value=${data[i].price} id="${data[i].Id}-price"></td>
        <td id="${data[i].Id}-miniPrice" class='amount'>${data[i].mini}</td>
        <td><input type="text" name="qty" value=${data[i].qty} id="${data[i].Id}-qty"></td>
        <td id="${data[i].Id}-productTotal" class='amount'>${data[i].productTotal}</td>
        <td id="${data[i].Id}-expectedPrice" class='amount'>${data[i].expected}</td>
        <td><button class="delete" id="${data[i].Id}-delete">Delete</button></td>`

        newrow.innerHTML = tds
        newrow.id = data[i].Id
        newrow.className = "salesrow"
    }
    addPriceEvent()
    grandtotal.innerHTML = addComas(total.toString())
    expectedGroundTotal.innerHTML = addComas(expectTotal.toString())
    const amounts = document.getElementsByClassName('amount')

    for (const node of amounts) {
        node.innerHTML = addComas(node.innerHTML.replace(/,/g, ''))
    }

}


try {
    const amounts = document.getElementsByClassName('amount')

    for (const node of amounts) {
        node.innerHTML = addComas(node.innerHTML.replace(/,/g, ''))
    }

} catch (error) {

}


// const setSalesCount = (data) => {
//     let cartPara = document.getElementById("sales")
//     cartPara.innerText = data.length
// }

const state = getState()
    // setSalesCount(state)
appendOrderList(state.cart)
setNumbering()
setCustomerData(state.customer)

const addToCartButtons = document.querySelectorAll(".addToCartButton")
addToCartButtons.forEach(button => {
    button.addEventListener("click", addOrder)
})

const selectBoxDiv = document.querySelectorAll(".selectBox")
selectBoxDiv.forEach(div => {
    div.addEventListener("click", showCheckboxes)
})
salesForm.addEventListener("submit", processOrder)
const get_user = document.getElementById("get_user")
get_user.addEventListener("click", getCustomer)

const updateUserState = (e) => {
    let target = e.target
    let customer = getState().customer
    customer[target.name] = target.value
    let storestate = storeReducer(addCustomer(customer))
    setState(storestate)

}
salesForm.elements.name.addEventListener('change', updateUserState)
salesForm.elements.phone_number.addEventListener('change', updateUserState)
salesForm.elements.email.addEventListener('change', updateUserState)
salesForm.elements.address.addEventListener('change', updateUserState)