const getSalesButton = document.getElementById("get_sales")
const getSalesForm = document.forms.getsales
const rootUrl = "http://127.0.0.1:8000"

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

getSalesButton.addEventListener('click', getsales)