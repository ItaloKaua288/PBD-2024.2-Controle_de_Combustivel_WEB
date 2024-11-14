let navbar_close_box = document.querySelector('.navbar-close-box');
navbar_close_box.addEventListener('click', (event)=>{
    document.querySelectorAll('.navbar-close-btn').forEach(element => {
        element.classList.toggle('d-none');
    });
    navbar_change();
});

function navbar_change() {
    let navbar = document.querySelector('#navbar')
    let options_box = document.querySelector('#options-box')
    if (navbar.style.width == '216px') {
        navbar.style.width = '89px'
        options_box.style.width = '73px'
        options_box.firstElementChild.style.paddingLeft = '13px'
    } else {
        navbar.style.width = '216px'
        options_box.style.width = '200px'
        options_box.firstElementChild.style.paddingLeft = '0'
    }
    document.querySelectorAll('.option-text').forEach(element => {
        element.classList.toggle('invisible')
    });
};