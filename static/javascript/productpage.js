const PriceEvent = (e) => {
    const Id = e.target.id.split("-")[0]
    const price = document.getElementById(`${Id}-price`)
    const qty = document.getElementById(`${Id}-qty`)
    const product_total = parseFloat(price.value) * parseFloat(qty.value)
    const productTotal = document.getElementById(`${Id}-productTotal`)
    const grandtotal = document.getElementById('grandtotal')
    productTotal.innerHTML = product_total
    const previousCart = getState().cart
    let total = 0
    previousCart.forEach(item => {
        if (item.Id == Id) {
            item.price = price.value;
            item.qty = qty.value;
            item.productTotal = product_total
        }
        total += item.productTotal
    })
    grandtotal.innerHTML = total
    storestate = storeReducer(UpdateCart(previousCart))
    setState(storestate)

}

const deleteEvent = (e) => {
    let target = e.target
    const Id = target.id.split("-")[0]
    const previousCart = getState().cart
    const grandtotal = document.getElementById('grandtotal')
    const productTotal = document.getElementById(`${Id}-productTotal`).innerHTML
    let parentNode = target.parentNode.parentNode
    grandtotal.innerHTML = parseFloat(grandtotal.innerHTML) - parseFloat(productTotal)
    parentNode.remove()
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
                product.Id = parseInt(`${product.id}${Id}`)
                product.qty = 1
                product.productTotal = parseFloat(price)
                productList.push(product)
                node.checked = false
            }
        })
        if (!selectionFound) {
            alert("No selection made, please make a selection.")
        }
    } else {
        let product = {}
        let [id, product_type, size, price, color, image] = list
        product.size = size
        product.price = parseFloat(price)
        product.id = parseInt(id)
        product.Id = parseInt(id)
        product.product_type = product_type
        product.color = color
        product.image = image
        product.qty = 1
        product.productTotal = parseFloat(price)
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


    UpdateCart
    storestate = storeReducer(addToCart(purelist))
    setState(storestate)
    const currentCart = getState().cart
    setSalesCount(currentCart)
    appendOrderList(purelist)
}

const processOrder = (e) => {
    const salesForm = document.forms.salesForm
    const data = {
        customer_name: salesForm.elements.customer_name.value,
        phone_number: salesForm.elements.phone_number.value,
        email: salesForm.elements.email.value,
        address: salesForm.elements.address.value,
        payment_method: salesForm.elements.payment_method.value,
        remark: salesForm.elements.remark.value,
    }
    console.log(data)
}
const appendOrderList = (data) => {
    let tbody = document.querySelector("#tbody")
    const grandtotal = document.getElementById('grandtotal')
    let total = parseFloat(grandtotal.innerHTML)
    for (let i = 0; i < data.length; i++) {
        total += data[i].productTotal
        let newrow = tbody.insertRow()
        let tds = ` <td class="counterCell"></td>
        <td>${data[i].product_type}</td>
        <td>${data[i].color}</td>
        <td>${data[i].size}</td>
        <td><input type="text" name="price" value=${data[i].price} id="${data[i].Id}-price"></td>
        <td><input type="text" name="qty" value=${data[i].qty} id="${data[i].Id}-qty"></td>
        <td id="${data[i].Id}-productTotal">${data[i].productTotal}</td>
        <td><button class="delete" id="${data[i].Id}-delete">Delete</button></td>`

        newrow.innerHTML = tds
        newrow.id = data[i].Id
        newrow.className = "salesrow"
    }
    addPriceEvent()
    grandtotal.innerHTML = total


}

const setSalesCount = (data) => {
    let cartPara = document.getElementById("sales")
    cartPara.innerText = data.length
}

const currentCart = getState().cart
setSalesCount(currentCart)
appendOrderList(currentCart)

const addToCartButtons = document.querySelectorAll(".addToCartButton")
addToCartButtons.forEach(button => {
    button.addEventListener("click", addOrder)
})

const selectBoxDiv = document.querySelectorAll(".selectBox")
selectBoxDiv.forEach(div => {
    div.addEventListener("click", showCheckboxes)
})
document.forms.salesForm.addEventListener("submit", processOrder)