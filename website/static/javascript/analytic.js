window.onload=function(){

    const toggleBtn = document.querySelector('.toggle_btn')
    const toggleBtnIcon = document.querySelector('.toggle_btn i')
    const dropDownMenu = document.querySelector('.dropdown_menu')


    const report_btn = document.querySelector("analytic-btn"); // Ensure the ID is correct
    console.log(report_btn); // Check if button is found
    if (report_btn) {
        report_btn.addEventListener("click", genReport);
    }


// const report_btn = document.querySelector('analytic-btn')
// console.log(`report button: ${report_btn}`)

    toggleBtnIcon.addEventListener('click', () => {
        dropDownMenu.classList.toggle('open')
        console.log('icon clicked')
    })

    async function genReport(){
        console.log('Pressed Create Report Button')
        try {
            const response = await fetch("/analytic_report",
                {method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            )
            result = await response.json();
            if (result.status === 'success') {
                //display success message
                console.log('Report generated successfully')
            } else {
                console.error(`Generation Failed: ${result.message}`);
            }
        } catch(e) {
            console.log(`Error: ${e}`)
        }
    }
// report_btn.addEventListener("click", genReport)
};