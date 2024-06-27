function hideFlash() {
    setTimeout(function() {
        var flashes = document.querySelectorAll('.alert-danger','.alert-success')
        flashes.forEach(function(flash){
            flash.style.display = 'none'
        })
    }, 2000)
}

hideFlash()
