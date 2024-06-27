
document.addEventListener('DOMContentLoaded', () => {
    const tags = document.querySelectorAll('.drop-down .button')
    const toggleBtn = document.querySelector('.toggle_btn')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const dropDownMenu = document.querySelector('.dropdown_menu')

    toggleBtnIcon.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open')
        console.log('icon clicked')
    })

    const dropDowns = document.querySelectorAll(".drop-down")
    dropDowns.forEach(dropDown => {
        const button = dropDown.querySelector('button');
        const stat = dropDown.querySelector('.stat');

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
    });

})


const orderByCardBtn = document.getElementById("card_btn")
const orderByDateBtn = document.getElementById("date_btn")

async function orderByCards(e) {
    try {
        if (!e.target.classList.contains("order_btn")) return;
        const data ={m: "card"}

        const response = await fetch("/fetch_order_change", 
            {   method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
        const result = await response.json();
        console.log(`Success: ${result}`)
    } catch(e){
        console.log(`Error" ${e}`)
    }
}

async function orderByDate(e) {
    try {
        if (!e.target.classList.contains("order_btn")) return;
        const data ={m: "date"}

        const response = await fetch("/fetch_order_change", 
            {   method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
        const result = await response.json();
        console.log(`Success: ${result}`)
    } catch(e){
        console.log(`Error" ${e}`)
    }
}

orderByCardBtn.addEventListener("click", orderByCards)
orderByDateBtn.addEventListener("click", orderByDate)
