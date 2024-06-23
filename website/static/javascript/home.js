
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



// const orgsList = document.querySelector(".orgs")
// const orderByCardBtn = document.getElementById("card_btn")
// const orderByDateBtn = document.getElementById("date_btn")
// const orgs = []

// async function orderByCards(e) {
//     try {
//         if (!e.target.classList.contains("order_btn")) return;
//         const letter = "card"
//     } catch(e){

//     }
// }

// async function orderByDate(e) {
//     try{
//         if(!e.target.classList.contains("order_btn")) return;
//         const letter = "date"
//     } catch(e){

//     }
// }

// orderByCardBtn.addEventListener("click", orderByCards)
// orderByDateBtn.addEventListener("click", orderByDate)
