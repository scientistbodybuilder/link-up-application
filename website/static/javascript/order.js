document.addEventListener('DOMContentLoaded', () => {
    const tags = document.querySelectorAll('.drop-down .button')
    const toggleBtn = document.querySelector('.toggle_btn')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const dropDownMenu = document.querySelector('.dropdown_menu')
    const form = document.getElementById("form")

    toggleBtnIcon.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open')
        console.log('icon clicked')
    })

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        
        
        lc_qty = document.getElementById("link-cards-qty").value
        dc_qty = document.getElementById("direct-cards-qty").value
        link_amt = document.getElementById("link-amount").value
        dc_url = document.getElementById("direct-cards-url").value
        link_list = []
        let link_amt_num
        let valid
        if (link_amt && isDigit(link_amt)){
            link_amt_num = Number(link_amt)
            for(let i=0; i< link_amt_num;i++){
                link_list.push(document.getElementById(`link-tree-url-${i}`).value)
            }
            valid = validOrder(dc_qty,lc_qty,link_amt_num,dc_url,link_list)
        } else {
            link_amt_num = 0
            valid = validOrder(dc_qty,lc_qty,link_amt_num,dc_url,link_list)
        }

        if (valid == 1) { //valid order, send to server
            console.log("Order is valid")
            alert = document.querySelector('.alert')
            if(alert.classList.contains('show')){
                alert.classList.remove('show')
            }         
            submitOrder(dc_qty,lc_qty,dc_url,link_list)
        } else if (valid == 2){ //not a valid order - display hints
            console.log("Did not provide direct url")
            alert = document.querySelector('.alert')
            alert.classList.add('show')
            alert.textContent = "Did not provide a direct URL"
        } else if(valid==3){
            console.log("Did not specify the link tree url amount")
            alert = document.querySelector('.alert')
            alert.classList.add('show')
            alert.textContent = "Did not specify the link tree URL amount"
        } else if(valid==4){
            console.log("A link tree url is missing / empty")
            alert = document.querySelector('.alert')
            alert.classList.add('show')
            alert.textContent = "A link tree URL is missing / empty"
        } else if(valid==0){
            console.log("Did not select a Link Tree or Direct Card")
            alert = document.querySelector('.alert')
            alert.classList.add('show')
            alert.textContent = "Did not select a link tree or direct card"
        }

    })
    })
    //FORM SUBMISSION
function isDigit(str) {
    return !isNaN(Number(str)) && Number(str) >= 0 && Number.isInteger(Number(str));
}

function validOrder(dc_qty,lc_qty,link_amt,dc_url,link_list) {
    const direct_card = (dc_qty && isDigit(dc_qty))
    const link_tree_card = (lc_qty && isDigit(lc_qty))
    if (direct_card || link_tree_card){
        if (direct_card){
            const d = Number(dc_qty)
            if (d>0){ //atleast one direct card
                if(dc_url == ''){
                    return 2
                }
            }
        }
        if (link_tree_card){
            const l = Number(lc_qty)
            if (l>0){ //atleast one link tree card
                if (link_amt < 1){
                    return 3
                } else {
                    for (let i=0;i<link_amt;i++){
                        if (link_list[i] == ''){
                            return 4
                        }
                    }
                }
            } 
        }
        return 1
    } else {
        return 0
    }
}
async function submitOrder(dc_qty, lc_qty, dc_url, link_list) {
    try {
        const response = await fetch("/submit-order", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ // Use 'body' instead of 'data'
                'direct-card-qty': dc_qty,
                'link-card-qty': lc_qty,
                'direct-card-url': dc_url,
                'link-tree-url': link_list
            })
        });
        
        const result = await response.json(); // Parse the response as JSON

        if ('status' in result) {
            const submissionHeader = document.querySelector('.submission-result');
            if (result['status'] == 'success') {
                console.log("Changing submission header");
                submissionHeader.textContent = "Order Submitted Successfully";
                form.reset(); // Clear the form inputs
            } else {
                console.log("Changing submission header");
                submissionHeader.textContent = 'Failed to Submit Order';
            }
        }
    } catch (e) {
        console.log(`Error order submission: ${e}`);
    }
}


//FORM RESPONSIVENESS

function linkTree(event){
    console.log("pressed")
    const linkNumber = event.target.value
    const linktreeURLContainer = document.getElementById('linktree-url')
    linktreeURLContainer.innerHTML = ''  //remove all the existing children
    for (let i=0; i< linkNumber; i++){  //add new children
        const urlBlock = document.createElement('textarea')
        urlBlock.setAttribute('placeholder','Enter Link Tree URL')
        urlBlock.setAttribute('name',`link-tree-url-${i}`)
        urlBlock.setAttribute('id',`link-tree-url-${i}`)

        linktreeURLContainer.appendChild(urlBlock)
    }
};


