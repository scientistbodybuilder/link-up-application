document.addEventListener('DOMContentLoaded', () => {
    const tags = document.querySelectorAll('.drop-down .button')
    const toggleBtn = document.querySelector('.toggle_btn')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const dropDownMenu = document.querySelector('.dropdown_menu')

    toggleBtnIcon.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open')
        console.log('icon clicked')
    })
})


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

        linktreeURLContainer.appendChild(urlBlock)
    }
};

