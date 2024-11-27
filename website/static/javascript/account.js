const accountInfoBtn = document.getElementById('acc_btn');
const orderHistorybtn = document.getElementById('ord_btn');
const accContainer = document.getElementById('acc-container');
const orderContainer = document.getElementById('order-container');

const modal1 = document.querySelector('.modal-confirm-password');
const overlay = document.getElementById('overlay');
const emailEditBtn = document.getElementById('edit-email');
const modalCloseBtn = document.querySelector('.close-pcm');
const modalCancelBtn = document.querySelector('.cancel-password-button');
const changePasswordBtn = document.getElementById('change-password')
const confirmPasswordBtn = document.getElementById('password-confirmation')

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.querySelector('.toggle_btn')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const dropDownMenu = document.querySelector('.dropdown_menu')

    toggleBtnIcon.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open')
        console.log('icon clicked')
    })
})

async function signout(){
    try {
        const data = {m: "account"}
        const response = await fetch("/acc_signout",
            {method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
        const result = await response.json();
        if (result.status === 'success') {
            window.location.href = result.redirect; // Perform the redirect
        } else {
            console.error(`Error: ${result.message}`);
        }

    } catch(e) {
        console.log(`Error: ${e}`);
    }
}


//GET PERSONAL INFORMATION

async function getInfo() {
    try {
        const email_field = document.querySelector('.email');
        const direct_card_field = document.getElementById('direct_card_purchased')
        const linktree_card_field = document.getElementById('linktree_card_purchased')

        const response = await fetch("/acc_get_info",
            {method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )

        const result = await response.json();
        email_field.textContent = result['email'];
        direct_card_field.textContent = `Direct Cards purchased: ${result['direct_card']}`;
        linktree_card_field.textContent = `Linktree Cards purchased: ${result['linktree_card']}`;
    } catch(e){
        console.log(`Error: ${e}`);
    }
}

getInfo()

async function orderInfo()
{
    try {
        const response = await fetch("/order-history",
            {method: 'POST',
                headers: {'Content-Type': 'application/json'}
            }
        )
        const result = await response.json();
        const orderScroll = document.querySelector('.scroll-box')
        orderScroll.innerHTML = '';
        result.forEach(order=>{
            const orderCard = document.createElement('div');
            orderCard.classList.add('order');

            orderCard.innerHTML = `
                    <p class="date">${order.date}</p>
                    <p class="num-LT">${order.LTcard}</p>
                    <p class="num-D">${order.Dcard}</p>
                    <p class="total">$${order.total}</p>
            `
            orderScroll.appendChild(orderCard);
        })
        console.log('complete rendering orders')
    } catch(e){
        console.log(`Error: ${e}`)
    }
}

// EDIT PERSONAL INFORMATION

changePasswordBtn.addEventListener("click", async ()=>{
    data = {
        form: 'password'
    }
    const response = await fetch("/render_edit_page", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await response.json();
    const url = result['page'];
    window.location.href=url;

})

confirmPasswordBtn.addEventListener("submit", async (e) => {
    e.preventDefault();
    const password = document.getElementById('confirm-password').value;
    
    const data = {
        form: 'email',
        check_password: password
    };
    try {
        const response = await fetch("/render_edit_page", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        const url = result['page'];
        window.location.href = url;
    } catch(e) {
        console.log(`Error: ${e}`)
    }
})

//TOGGLE BETWEEN ACCOUT VIEWS AND ORDER HISTORY

function loadAccount(){
    console.log('load account')
    accContainer.style.display = "block";
    orderContainer.style.display = "none";
}

function loadOrder(){
    console.log('load order')
    accContainer.style.display = "none";
    orderContainer.style.display = "block";
}


//MODAL FUNCTIONALITY
function openModal1() {
    console.log("open modal clicked");
    modal1.classList.add('active');
    overlay.classList.add('active');
    //why not toggle?
}

function closeModal1() {
    console.log("close modal clicked");
    modal1.classList.remove('active');
    overlay.classList.remove('active');
}

emailEditBtn.addEventListener("click", openModal1);
modalCloseBtn.addEventListener("click", closeModal1);
modalCancelBtn.addEventListener("click", closeModal1);
overlay.addEventListener("click", closeModal1);

accountInfoBtn.addEventListener("click", async () => {
    console.log("loading accout info")
    try{
        loadAccount()
        await getInfo()
    } catch(e){
        console.log(`Error: ${e}`)
    }
}) 
orderHistorybtn.addEventListener("click", async ()=> {
    console.log("loading order info")
    try {
        loadOrder()
        await orderInfo()
    } catch(e){
        console.log(`Error: ${e}`)
    }
})