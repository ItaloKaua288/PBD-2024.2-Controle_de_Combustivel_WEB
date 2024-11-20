document.querySelector('.navbar-close-box').addEventListener('click', ()=>{
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
        options_box.style.maxWidth = '73px'
        options_box.firstElementChild.style.paddingLeft = '13px'
    } else {
        navbar.style.width = '216px'
        options_box.style.maxWidth = '200px'
        options_box.firstElementChild.style.paddingLeft = '0'
    }
    dropdownMenu_change()
    document.querySelectorAll('.option-text').forEach(element => {
        element.classList.toggle('invisible')
    });
};
 
document.querySelectorAll('.dropdown').forEach(element => {
    element.addEventListener('mouseover', ()=>{
        element.lastElementChild.style.display = 'block'
    });
    element.addEventListener('mouseout', ()=>{
        element.lastElementChild.style.display = 'none'
    });
});

function dropdownMenu_change() {
    let dropdown_menus = document.querySelectorAll('.dropdown-menu')
    dropdown_menus.forEach(element => {
        if (element.style.left == '55px')
            element.style.left = '175px'
        else
            element.style.left = '55px'
    });
}