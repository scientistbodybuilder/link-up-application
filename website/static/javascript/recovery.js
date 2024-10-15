const submitBtn = document.getElementById("submitBtn");
const word = document.querySelector('.word');
submitBtn.addEventListener("submit", async ()=>{
    word.textContent = "This process may take up to 5 minutes";
    submitBtn.value = "Resend";
    const element = document.querySelector('.success')
    element.classList.add('show')
    
})
