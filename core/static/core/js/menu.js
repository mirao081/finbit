const menuBtn=document.getElementById("menuBtn");
const closeBtn=document.getElementById("closeMenu");
const sideMenu=document.getElementById("sideMenu");
const overlay=document.getElementById("overlay");
function openMenu(){

    sideMenu.classList.add("active");
    overlay.classList.add("active");
}
function closeMenu(){
    sideMenu.classList.remove("active");
    overlay.classList.remove("active");
}
menuBtn.addEventListener("click",openMenu);
closeBtn.addEventListener("click",closeMenu);
overlay.addEventListener("click",closeMenu);