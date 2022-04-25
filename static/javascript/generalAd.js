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

document.getElementsByTagName("BODY")[0].onscroll = function() {
    backToTop()
};
document.getElementsByTagName("BODY")[0].onresize = function() {
    myResize()
};

window.addEventListener('scroll', function() {
    backToTop()
});

try {
    const deleteButtons = document.getElementsByClassName('delete')

    const ConfirmDelete = (e) => {
        e.preventDefault()
        const check = confirm("Are you Sure you want to delete")
        if (check) {
            window.location.href = e.target.parentNode.href
        }
    }

    for (const button of deleteButtons) {
        button.addEventListener("click", ConfirmDelete)

    }

} catch (error) {

}