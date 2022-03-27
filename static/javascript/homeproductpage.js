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
    const previousCart = getState().user_cart
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
    storestate = storeReducer(addToCart(purelist, "user_cart"))
    setState(storestate)
        //const currentCart = getState().cart
    setSalesCount(storestate.user_cart)
        // appendOrderList(purelist)
}


const processOrder = (e) => {
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
        total_amount: grandtotal.innerHTML,
        expected_amount: expectedGroundTotal.innerHTML,
        purchase_id: OrderId,
        orders: getState().user_cart
    }
    if (data.orders.length > 0) {
        if (data.total_amount >= data.expected_amount) {
            ProcessOrder(data, csrtoken).then(data => {
                    setState(storeReducer(addLatestOrder(data)))
                    manageLastSale(data)
                    let rows = tbody.children
                    grandtotal.innerHTML = ""
                    salesForm.elements.name.value = ""
                    salesForm.elements.phone_number.value = ""
                    salesForm.elements.email.value = ""
                    salesForm.elements.address.value = ""
                    salesForm.elements.payment_method.value = ""
                    salesForm.elements.remark.value = ""
                    grandtotal.innerHTML = ""
                    expectedGroundTotal.innerHTML = ""
                    for (const row of rows) {
                        row.remove()
                    }
                })
                .catch((error) => {
                    alert(error)
                    setState(storeReducer(load(LOADED)))
                });
        } else {
            alert("You are selling below the expected price")
        }
    } else {
        alert("No product selected")
    }

    // console.log(JSON.stringify(data))
}

const setSalesCount = (data) => {
    let cartPara = document.getElementById("cart_count")
    cartPara.innerText = data.length
}

setSalesCount(getState().user_cart)

const addToCartButtons = document.querySelectorAll(".addToCartButton")
addToCartButtons.forEach(button => {
    button.addEventListener("click", addOrder)
})

const selectBoxDiv = document.querySelectorAll(".selectBox")
selectBoxDiv.forEach(div => {
    div.addEventListener("click", showCheckboxes)
})