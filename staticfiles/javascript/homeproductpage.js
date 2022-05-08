let csrtoken = undefined
const toggle = document.getElementById("toggle")
const closeButton = document.getElementById("close")


copyRightDate(2020)

function copyRightDate(x) {
    var d = new Date;
    var year = d.getFullYear();
    var footerDate = document.getElementById("footerdate");
    if (year == x) {
        footerDate.innerHTML = year;
    } else {
        footerDate.innerHTML = x + "-" +
            year;
    }
}

try {
    csrtoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
} catch (error) {

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

let display = false
const handleToggle = () => {
    const sideNav = document.querySelector('.sideNav')
    display = !display
    if (display) {
        sideNav.id = 'mobile'
        closeButton.style.display = 'block'
    } else {
        sideNav.id = 'sideNav'
        closeButton.style.display = 'none'
    }
}

toggle.addEventListener("click", handleToggle)
closeButton.addEventListener("click", handleToggle)


const backToTop = () => {
    let y_axis_offset = window.pageYOffset ||
        document.documentElement.scrollTop ||
        document.body.scrollTop;
    x = "300";
    let backToTopButton = document.getElementById("backToTop");
    if (y_axis_offset >= x) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
}


let SafariDetector = !/function/.test(window.HTMLElement)

const myResize = () => {
    const sideNav = document.querySelector('.sideNav')
        // let x_axis = window.innerWidth;
    sideNav.id = 'sideNav'
    closeButton.style.display = 'none'
    display = false

}


// const myResizeSafari = () => {
//     const sideNav = document.querySelector('.sideNav')
//     let x_axis = document.documentElement.clientWidth ||
//         document.body.clientWidth;
//     if (x_axis <= 999) {
//         sideNav.id = 'mobile'
//     } else {
//         sideNav.id = 'sideNav'
//     }
// }

document.getElementsByTagName("BODY")[0].onscroll = function() {
    backToTop()
};
document.getElementsByTagName("BODY")[0].onresize = function() {
    myResize()
};

window.addEventListener('scroll', function() {
    backToTop()
});
// window.addEventListener('resize', function() {
//     myResizeSafari()
// });




const handleDecisionBox = () => {
    const decisionBox = document.getElementById('decisionBox')
    let x_axis = document.documentElement.clientWidth ||
        document.body.clientWidth;
    if (x_axis >= 1000) {
        let num = (x_axis - 780) / 2
        decisionBox.style.marginLeft = `${num}px`
    } else {
        let num = (x_axis - 332) / 2
        decisionBox.style.marginLeft = `${num}px`
    }
    decisionBox.style.display = 'block'
}

const Alert = (text) => {
    const alertBox = document.getElementById('alertBox')
    const displayText = document.getElementById('displayText')
    let x_axis = document.documentElement.clientWidth ||
        document.body.clientWidth;
    if (x_axis >= 1000) {
        let num = (x_axis - 780) / 2
        alertBox.style.marginLeft = `${num}px`
    } else {
        let num = (x_axis - 332) / 2
        alertBox.style.marginLeft = `${num}px`
    }
    alertBox.style.display = 'block'
    displayText.innerHTML = text
}


const handleCloseAlert = () => {
    const alertBox = document.getElementById('alertBox')
    alertBox.style.display = 'none'

}

const handleCheckout = (e) => {
    e.preventDefault()
    const decisionBox = document.getElementById('decisionBox')
    decisionBox.style.display = 'none'
    window.location.href = `/cart`

}

try {
    const closeAlert = document.querySelector('#closeAlert')
    closeAlert.addEventListener("click", handleCloseAlert)
    const checkout = document.querySelector('.checkout')
    checkout.addEventListener('click', (e) => handleCheckout(e))

} catch (error) {

}


const continueShopping = (e) => {
    e.preventDefault()
    const decisionBox = document.getElementById('decisionBox')
    decisionBox.style.display = 'none'
}

try {
    const continueButton = document.querySelector('.continue')
    continueButton.addEventListener('click', (e) => continueShopping(e))
} catch (error) {

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
            Alert("No selection made, please make a selection.")
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
                Alert(`${product.product_type} ${product.color} ${product.size} already added `)
            }
        });
    } else {
        purelist = productList;
    }


    // UpdateCart
    if (productList.length > 0) {
        handleDecisionBox()
        storestate = storeReducer(addToCart(purelist, "user_cart"))
        setState(storestate)
            //const currentCart = getState().cart
        setSalesCount(storestate.user_cart)
            // appendOrderList(purelist)

    }

}


const showOrderHistoryButton = (data = null) => {
    let hidden_phone_number = undefined
    try {
        hidden_phone_number = document.getElementById("hidden_phone_number")
        const phone_number = data ? data : getState().customerphone_number
        if (phone_number != "" && phone_number != null) {
            hidden_phone_number.value = phone_number
        }
    } catch (error) {

    }
}
showOrderHistoryButton(getState().customer.phone_number)

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

const amounts = document.getElementsByClassName('amount')

for (const node of amounts) {
    node.innerHTML = addComas(node.innerHTML)
}


function SearchFunction() {
    var input, filter, product, contents, i;
    input = document.getElementById("filterInput");
    filter = input.value.toUpperCase();
    product = document.getElementsByClassName("product");
    for (i = 0; i < product.length; i++) {
        contents = product[i].getElementsByTagName("h3")[0];
        if (contents.innerHTML.toUpperCase().indexOf(filter) > -1) {
            product[i].style.display = "block";
        } else {
            product[i].style.display = "none";

        }
    }
}

try {
    const filterInput = document.getElementById('filterInput')
    filterInput.addEventListener('keyup', SearchFunction)
} catch (error) {

}