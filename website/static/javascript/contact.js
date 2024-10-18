document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.querySelector('.toggle_btn')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const dropDownMenu = document.querySelector('.dropdown_menu')
    const form = document.getElementById("form")

   

    toggleBtnIcon.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open')
        console.log('icon clicked')
    })
    form.addEventListener('submit', async (event) => {
        event.preventDefault()
        try {
            const textbox = document.getElementById('message')
            const text = textbox.value
            const data = {'msg': text}
            const response = await fetch("/contact-message",
                {method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }, body: JSON.stringify(data)
                }
            )

            const result = await response.json()
            const sentField = document.getElementById('sent')
            if (result['status'] == 'success'){
                //show 'message sent'
                console.log("message sent")
                textbox.textContent = ""
                sentField.textContent = "Message sent"


            } else {
                //show 'failed to send message
                console.log("message not sent")
                sentField.textContent = "Failed to send message"
            }
        } catch(e){
            console.log(`Error: ${e}`)
        }
        
    })
})


async function signout(){
    try {
        const data = {m: "contact"}
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