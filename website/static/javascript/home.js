const toggleBtn = document.querySelector('.toggle_btn')
const toggleBtnIcon = document.querySelector('.toggle_btn i')
const dropDownMenu = document.querySelector('.dropdown_menu')

toggleBtnIcon.addEventListener('click', () => {
    dropDownMenu.classList.toggle('open')
    console.log('icon clicked')
})

const orderByCardBtn = document.getElementById("card_btn")
const orderByDateBtn = document.getElementById("date_btn")

async function updateOrder(method){
    try {
        const data = {m: method};
        console.log("I was clicked");
        const response = await fetch("/fetch_order_change",
            {method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
        const result = await response.json();
        if ('status' in result){
            console.log(result);
            return;
        }
        const orgCardcontainer = document.querySelector(".orgs");
        orgCardcontainer.innerHTML = '';
        result.forEach(card=>{
            const cardElement = document.createElement('div');
            cardElement.classList.add('drop-down');

            cardElement.innerHTML = `
                <button> ${card.name} </button>
                <div class="stat">
                    <p>Cards in use: ${card.card_num } </p>
                    <p>Date joined: ${card.date }</p>
                </div>
            `;

            const button = cardElement.querySelector('button');
            const stat = cardElement.querySelector('.stat');
            button.addEventListener('click', function () {
                console.log("dropdown clicked")
                if(!this.dataset.clicked){
                    this.setAttribute("data-clicked", "true");
                    stat.style.display = "block"
                } else {
                    this.removeAttribute("data-clicked")
                    stat.style.display = "none"
                }
            });

            orgCardcontainer.appendChild(cardElement);
        })

    } catch(e){
        console.log(`Error: ${e}`);
    }
}

async function signout(){
    try {
        const data = {m: "home"}
        const response = await fetch("/view_signout",
            {method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
        result = await response.json();
        if (result.status === 'success') {
            window.location.href = result.redirect; // Perform the redirect
        } else {
            console.error(`Error: ${result.message}`);
        }

    } catch(e){
        console.log(`Error: ${e}`);
    }
}

updateOrder("card");

orderByCardBtn.addEventListener("click", () => updateOrder("card"));
orderByDateBtn.addEventListener("click", () => updateOrder("date"));

