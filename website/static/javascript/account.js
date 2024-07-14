const accountInfoBtn = document.getElementById('acc_btn');
const orderHistorybtn = document.getElementById('ord_btn');
const modal1 = document.querySelector('.modal-confirm-password');
const overlay = document.getElementById('overlay');
const emailEditBtn = document.getElementById('edit-email');
const modalCloseBtn = document.querySelector('.close-pcm');

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

        const response = await fetch("/acc_get_info",
            {method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )

        const result = await response.json();
        email_field.textContent = result['email']
    } catch(e){
        console.log(`Error: ${e}`);
    }
}

getInfo()

// EDIT PERSONAL INFORMATION

async function edit(load){
    try {
        if (load == "accout"){

        } else {

        }
    } catch(e) {
        console.log(`Error: ${e}`)
    }
}


//TOGGLE BETWEEN ACCOUT VIEWS AND ORDER HISTORY

async function loadAccount(){

}

async function loadOrder(){
    
}

accountInfoBtn.addEventListener("click", loadAccount);
orderHistorybtn.addEventListener("click", loadOrder);

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
overlay.addEventListener("click", closeModal1);