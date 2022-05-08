const order_id = document.getElementById("order_id")
const payment_method = document.getElementById("payment_method")
let get_sale_button = undefined
let getSalesButton = undefined
let getSalesForm = undefined

try {
    getSalesButton = document.getElementById("get_sales")
    getSalesForm = document.forms.getsales
    get_sale_button = document.getElementById("get_sale")
} catch (error) {

}

const rootUrl = "http://127.0.0.1:8000"

const setNumbering = (id = undefined) => {
    let sn = undefined
    if (id) {
        sn = document.getElementsByClassName("sn" + id)
    } else {
        sn = document.getElementsByClassName("sn")
    }

    let num = 1
    for (const td of sn) {
        td.innerHTML = num++
    }
}

try {
    setNumbering()
    setNumbering('1')
    setNumbering('2')
    setNumbering('3')
    setNumbering('4')
} catch (error) {

}

const getsales = (e) => {
    e.preventDefault()
    const branch = getSalesForm.elements.branch.value
    const start_date = getSalesForm.elements.start_date.value
    const end_date = getSalesForm.elements.end_date.value

    if (start_date === "" && end_date === "") {
        alert("Please make sure that start and end dates are not empty")
    } else {
        if (start_date == end_date) {
            window.location.href = `/sales/${start_date}/${branch}/analysis`
        } else {
            window.location.href = `/sales/${start_date}/${end_date}/${branch}/rangeanalysis`
        }
    }
}



const getSale = () => {
    const orderId = order_id.value.trim()
    const paymentMethod = payment_method.value
    if (orderId == "" && paymentMethod == "") {
        alert("Please enter order Id and select a mode of transaction")
    } else {
        window.location.href = `/sales/sale/${orderId}/${paymentMethod}`
    }
}

try {
    getSalesButton.addEventListener('click', getsales)
    get_sale_button.addEventListener('click', getSale)
} catch (error) {

}



const addComas = (input) => {

    const mutate = (array, result = []) => {
        if (array.length < 3) {
            if (array.length > 0) {
                result.push(array)
            }

            return result
        }

        const LastThree = array.slice(-3, )
        result.push(LastThree)
        const lastIndex = array.length - 3
        const remaining = array.slice(0, lastIndex)
        mutate(remaining, result)
        return result
    }

    let result = ""
    const [first, second] = input.split(".")
    const firstNum = mutate(first)
    const firstHalf = firstNum.reverse().join(",")

    if (second == undefined) {
        result = firstHalf
    } else {
        result = `${firstHalf}.${second}`
    }
    return result

}

try {
    const amounts = document.getElementsByClassName('amount')

    for (const node of amounts) {
        if (node.innerHTML.toLowerCase() != 'none') {
            node.innerHTML = addComas(node.innerHTML.replace(/,/g, ''))
        }

    }

} catch (error) {

}