//Action Types
const ADD_TO_CART = "ADD_TO_CART";
const UPDATE_CART = "UPDATE_CART";
const CLEAR_CART = "CLEAR_CART";
const CLEAR_USER_CART = 'CLEAR_USER_CART';
const ADD_TO_USER_CART = "ADD_TO_USER_CART";
const UPDATE_USER_CART = "UPDATE_USER_CART";
const PROCESS_ORDER = "PROCESS_ORDER";
const ADD_LATEST_ORDER = "ADD_LATEST_ORDER";
const rootUrl = "https://smbclassic.com.ng";
const LOADED = "LOADED";
const LOADING = "LOADING";
const ADD_ERROR = "ADD_ERROR";
const ADD_CUSTOMER = "ADD_CUSTOMER";

const addToCart = (data, action = "cart") => {
    if (action == 'cart') {
        return {
            type: ADD_TO_CART,
            data: data
        }
    } else if (action == "user_cart") {
        return {
            type: ADD_TO_USER_CART,
            data: data
        }
    }

}

const clearCart = (action = "cart") => {
    if (action == 'cart') {
        return {
            type: CLEAR_CART
        }
    } else if (action == "user_cart") {
        return {
            type: CLEAR_USER_CART
        }
    }

}

const UpdateCart = (data, action = 'cart') => {
    if (action == "cart") {
        return {
            type: UPDATE_CART,
            data: data
        }
    } else if (action == "user_cart") {
        return {
            type: UPDATE_USER_CART,
            data: data
        }
    }

}

const addLatestOrder = (data) => {
    return {
        type: ADD_LATEST_ORDER,
        data: data
    }
}

const addCustomer = (data) => {
    return {
        type: ADD_CUSTOMER,
        data: data
    }
}

const load = (type) => {
    return {
        type: type
    }
}

const getState = () => {
    const localdata = localStorage.getItem("storestate");
    let finaldata = ""
    if (localdata) {
        const jsonify = JSON.parse(localdata)
        finaldata = {
            // User: "",
            loading: false,
            // logged: false,
            cart: [],
            user_cart: [],
            latestOrder: { "purchase_id": "", "type": "" },
            customer: { address: "", email: "", name: "", id: "", phone_number: "" },
            // success: false,
            // locations: [],
            // destination: "",
            // customer: { address: "", email: "", fullName: "", id: "", phone_number: "" },
            // logistics: 0,
            ...jsonify,
            // message: "",
            // status: "",
            // messages: "",
            // check: "",
        }
    } else {
        finaldata = {
            // User: "",
            loading: false,
            // logged: false,
            user_cart: [],
            cart: [],
            latestOrder: { "purchase_id": "", "type": "" },
            customer: { address: "", email: "", name: "", id: "", phone_number: "" },
            // success: false,
            // locations: [],
            // destination: "",
            // logistics: 0,
            // message: "",
            // status: "",
            // messages: "",
            // check: "",
        }
    }
    return finaldata
}

//Reducer
const storeReducer = (action) => {
    let state = getState()
    switch (action.type) {

        case ADD_TO_CART:
            return {
                ...state,
                cart: [...state.cart, ...action.data],
                loading: false,
            }

        case UPDATE_CART:
            return {
                ...state,
                cart: [...action.data],
                loading: false,
            }

        case CLEAR_CART:
            return {
                ...state,
                cart: [],
                loading: false,
            }

        case CLEAR_USER_CART:
            return {
                ...state,
                user_cart: [],
                loading: false,
            }

        case ADD_TO_USER_CART:
            return {
                ...state,
                user_cart: [...state.user_cart, ...action.data],
                loading: false,
            }

        case UPDATE_USER_CART:
            return {
                ...state,
                user_cart: [...action.data],
                loading: false,
            }

        case ADD_CUSTOMER:
            return {
                ...state,
                customer: action.data,
                loading: false,
            }

        case ADD_LATEST_ORDER:
            return {
                ...state,
                cart: [],
                // success: true,
                latestOrder: action.data,
                customer: { address: "", email: "", name: "", id: "", phone_number: "" },
                loading: false,
            }
        case LOADING:
            return {
                ...state,
                loading: true
            }
        case LOADED:
            return {
                ...state,
                loading: false,
            }

        default:
            return {
                ...state
            }
    }
}

const setState = (storestate) => {
    localStorage.setItem("storestate", JSON.stringify(storestate))
}

const ProcessOrder = async(data, token, url = '/sales/process') => {
    setState(storeReducer(load(LOADING)))
    let response = await fetch(url, {
        method: 'POST', // or 'PUT'
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify(data),
    })

    if (!response.ok) {
        throw new Error(response.statusText)
    }
    return await response.json()
}


// const getOrder = async(data) => {
//     setState(storeReducer(load(LOADING)))
//     let response = await fetch('/sales/csales', {
//         method: 'POST', // or 'PUT'
//         credentials: 'same-origin',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data),
//     })

//     if (!response.ok) {
//         throw new Error(response.statusText)
//     }
//     return await response.json()
// }

const GetCustomer = async(data, token) => {
    setState(storeReducer(load(LOADING)))
    let response = await fetch(`${rootUrl}/user/customer/0/get`, {
        method: 'POST', // or 'PUT'
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify(data),
    })

    if (!response.ok) {
        throw new Error(response.statusText)
    }
    return await response.json()
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


const convertToFloat = (input) => {
    return parseFloat(input.replace(/,/g, ''))

}



//   const getHours = (time) => {

//     let hours = time.slice(0, 2);
//     let covHours = parseInt(hours) + 1
//     let minutes = time.slice(3, 5);
//     let mins = minutes.length < 2 ? "0" + minutes : minutes

//     let amPM = covHours >= 12 && covHours !== "00" ? "PM" : "AM";
//     if (hours === "00") {
//         return 12 + ":" + mins + " " + amPM
//     } else if (covHours > 12) {
//         return covHours - 12 + ":" + mins + " " + amPM
//     } else {
//         return covHours + ":" + mins + " " + amPM
//     }
// }

//   const refreshPage = () => {
//         window.location.reload(true)
//     }