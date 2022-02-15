//Action Types
const ADD_TO_CART = "ADD_TO_CART";
const UPDATE_CART = "UPDATE_CART";
//   const PROCESS_ORDER = "PROCESS_ORDER";
//   const GET_PRODUCT_AND_CUSTOMER = "GET_PRODUCT_AND_CUSTOMER"
//   const LOADED = "LOADED";
//   const LOADING = "LOADING";
//   const ADD_ERROR = "ADD_ERROR";
//   const SUCCESS = "SUCCESS";
//   const CLEAR_SUCCESS = "CLEAR_SUCCESS";
//   const DELETE_MESSAGES = "DELETE_MESSAGES";
//   const PAYMENT = "PAYMENT";
//   const GET_LOCATION = "GET_LOCATION";
//   const ADD_LOGISTICS = "ADD_LOGISTICS";
//   const ADD_DESTINATION = "ADD_DESTINATION";
//   const ADD_NOTIFICATION = "ADD_NOTIFICATION";
//   const CLEAR_NOTIFICATION = "CLEAR_NOTIFICATION"
//   const GET_CUSTOMERS = "GET_CUSTOMERS"

//Capitalise first word
// const sentenceCase = (data) => {
//     let firstWord = data.slice(0, 1).toUpperCase()
//     let rest = data.slice(1).toLowerCase()
//     return `${firstWord}${rest}`
// }


// const filteritems = (array) => {
//     let result = []
//     array.forEach(item => result.push(...item))
//     return result
// }

//Actions dispatchers

// const processOrder = (data, config) => {
//     return axios.post('https://lameloapi.herokuapp.com/orderview', data, config).then(res => {
//         return {
//             type: PROCESS_ORDER,
//             data: res.data.Ordered,
//             success: true,
//             cart: [],
//             toppingcart: [],
//             user: res.data.user
//         }
//     }).catch(err => {
//         return {
//             type: ADD_ERROR,
//             data: err.response.data,
//             status: err.response.status
//         }

//     })
// }



// const payment = (data, orderlist) => {
//     return axios.post("https://lameloapi.herokuapp.com/payment", data, ).then(res => {
//         const filtered = orderlist.filter(item => item.id != res.data.id)
//         filtered.push(res.data)
//         return {
//             type: PAYMENT,
//             data: filtered

//         }
//     }).catch(err => {
//         return {
//             type: ADD_ERROR,
//             data: err.response.data,
//             status: err.response.status
//         }

//     })
// }

// const locations = () => {
//     return axios.get("https://lameloapi.herokuapp.com/location").then(res => {
//         return {
//             type: GET_LOCATION,
//             data: res.data
//         }
//     }).catch(err => {
//         return {
//             type: ADD_ERROR,
//             data: err.response.data,
//             status: err.response.status
//         }

//     })
// }


const addToCart = (data) => {
    return {
        type: ADD_TO_CART,
        data: data
    }
}


const UpdateCart = (data) => {
        return {
            type: UPDATE_CART,
            data: data
        }
    }
    // const load = (type) => {
    //     return {
    //         type: type
    //     }
    // }
    // const success = () => {
    //     return {
    //         type: SUCCESS
    //     }
    // }
    // const AddLogistics = (data) => {
    //     return {
    //         type: ADD_LOGISTICS,
    //         data: data
    //     }
    // }
    // const AddDestination = (data) => {
    //     return {
    //         type: ADD_DESTINATION,
    //         data: data
    //     }
    // }

// state
const getState = () => {
    const localdata = localStorage.getItem("storestate");
    let finaldata = ""
    if (localdata) {
        const jsonify = JSON.parse(localdata)
        finaldata = {
            // User: "",
            // loading: true,
            // logged: false,
            cart: [],
            // locations: [],
            // destination: "",
            // customer: { address: "", email: "", fullName: "", id: "", phoneNumber: "" },
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
            // loading: true,
            // logged: false,
            cart: [],
            // locations: [],
            // destination: "",
            // customer: { address: "", email: "", fullName: "", id: "", phoneNumber: "" },
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

            // case LOADING:
            //     return {
            //         ...state,
            //         loading: true
            //     }
            // case LOADED:
            //     return {
            //         ...state,
            //         loading: false,
            //     }
            // case PROCESS_ORDER:
            //     return {
            //         ...state,
            //         Ordered: [action.data, ...state.Ordered],
            //         success: action.success,
            //         cart: action.cart,
            //         toppingcart: action.toppingcart,
            //         User: action.user,
            //         logistics: 0,
            //         destination: "",
            //         loading: false,
            //     }
            // case PAYMENT:
            //     return {
            //         ...state,
            //         Ordered: action.data,
            //         loading: false
            //     }
            // case GET_LOCATION:
            //     return {
            //         ...state,
            //         locations: action.data,
            //         loading: false,
            //     }
            // case ADD_LOGISTICS:
            //     return {
            //         ...state,
            //         logistics: action.data,
            //         loading: false,
            //     }
            // case ADD_DESTINATION:
            //     return {
            //         ...state,
            //         destination: action.data,
            //         loading: false,
            //     }

            // case ADD_NOTIFICATION:
            //     return {
            //         ...state,
            //         notification: [...action.neworder, ...state.notification],
            //         Orders: action.data,
            //         customers: action.customers,
            //         loading: false,
            //     }
            // case CLEAR_NOTIFICATION:
            //     return {
            //         ...state,
            //         notification: [],
            //     }
            // case CLEAR_SUCCESS:
            //     return {
            //         ...state,
            //         success: false,
            //         loading: false,
            //     }
            // case SUCCESS:
            //     return {
            //         ...state,
            //         success: true,
            //         loading: false,
            //     }
            // case ADD_ERROR:
            //     return {
            //         ...state,
            //         message: action.data,
            //         status: action.status,
            //         loading: false,
            //     }
            // case DELETE_MESSAGES:
            //     return {
            //         ...state,
            //         message: "",
            //         status: "",
            //         messages: ""
            //     }
        default:
            return {
                ...state
            }
    }
}

const setState = (storestate) => {
    localStorage.setItem("storestate", JSON.stringify(storestate))
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