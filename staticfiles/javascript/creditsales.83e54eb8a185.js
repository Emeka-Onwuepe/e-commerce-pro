const order_id = document.getElementById("order_id")
const payment_method = document.getElementById("payment_method")
try {
    const get_sale_button = document.getElementById("get_sale")

    const getSale = () => {
        const orderId = order_id.value.trim()
        const paymentMethod = payment_method.value
        if (orderId == "" && paymentMethod == "") {
            alert("Please enter order Id and select a mode of transaction")
        } else {
            window.location.href = `/sales/sale/${orderId}/${paymentMethod}`
        }
    }

    get_sale_button.addEventListener('click', getSale)
} catch (error) {

}

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
} catch (error) {

}

const add_Comas = (input) => {

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
            node.innerHTML = add_Comas(node.innerHTML.replace(/,/g, ''))
        }

    }

} catch (error) {

}