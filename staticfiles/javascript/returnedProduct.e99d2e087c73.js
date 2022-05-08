const unit_price = document.getElementById("id_unit_price")
const qty = document.getElementById("id_qty")
const total_price = document.getElementById("id_total_price")
const Form = document.forms.Form
const amounts = document.getElementsByClassName('amount')

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


const convertToFloat = (input) => {
    return parseFloat(input.replace(/,/g, ''))
}

const calTotal = () => {
    let unitPrice = convertToFloat(unit_price.value)
    let amount = addComas(unitPrice.toString())
    unit_price.value = amount != 'NaN' ? amount : ""
    let total = unitPrice * parseInt(qty.value)
    total_price.value = addComas(total.toString())
}

const cleanForm = (e) => {

    const totalPrice = total_price.value
    const unitPrice = unit_price.value


    if (totalPrice == 'NaN') {
        alert("please check the Unit Price and qty")
        e.preventDefault()
    } else {
        const button = document.getElementById('button')
        button.disabled = true
            // total_price.type = "number"
            // unit_price.type = 'number'
        total_price.value = totalPrice.replace(/,/g, '')
        unit_price.value = unitPrice.replace(/,/g, '')
    }

}

for (const node of amounts) {
    node.innerHTML = addComas(node.innerHTML)
}

unit_price.addEventListener('change', calTotal)
qty.addEventListener('change', calTotal)
unit_price.addEventListener('keyup', calTotal)
qty.addEventListener('keyup', calTotal)


Form.addEventListener('submit', cleanForm)