let comment=document.querySelector('.comment'),
    xclick=document.querySelector('.splice'),
    comment_block=document.querySelector('.com');
let
    nav=document.querySelector('.introduction_entrance'),
    ham = document.querySelector('.hamburger_icon i');
comment.addEventListener('click',()=>{
    comment_block.classList.add('active1')
})
xclick.addEventListener('click',()=>{
    comment_block.classList.remove('active1')
})
ham.addEventListener('click', () => {

    if (ham.className === "fa-solid fa-bars"){
        ham.className = 'fa-solid fa-xmark'
    }else {
        ham.className = "fa-solid fa-bars"
    }
    nav.classList.toggle('active_menu')
})