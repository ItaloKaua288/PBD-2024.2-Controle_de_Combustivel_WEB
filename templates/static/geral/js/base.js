document.querySelector('.navbar-toggler-icon').addEventListener('click', sidemenu_change)

function sidemenu_change() {
    let sidemenu = document.querySelector('.sidebar')
    
    if (sidemenu.style.transform == ''){sidemenu.style.cssText = 'transform: translate3d(0, 0, 0) !important;!i;!;'}
    else {sidemenu.style.cssText = 'transform: translate3d(-273, 0, 0) !important;!i;!;'}
        
}
