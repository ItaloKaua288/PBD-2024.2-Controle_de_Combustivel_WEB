function popup(link, width, height) {
    window.open(link, '_blank', `width=${width},height=${height}`)
}

function move_btns() {
    let lista_choices = document.querySelectorAll('select')
    let btns = document.querySelectorAll('.add_btn')
    btns.forEach(btn => {
        lista_choices.forEach(select => {
            if (btn.id.toLowerCase().includes(select.name)) {
                select.parentNode.innerHTML += btn.parentNode.innerHTML
                btn.remove()
            }
        });
    });
}