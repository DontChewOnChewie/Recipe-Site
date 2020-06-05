let curImg = 1;
const maxImg = 4;
let main, transition_div;

/*
    Start and manage sliedshow.
*/
function slideshow() {
    setInterval(function() {
        transition_div.style.opacity = "1";
        setTimeout(function() {
            main.className = `bg${curImg}`
            setTimeout(function() {
                transition_div.style.opacity = "0"
            }, 300);
        }, 800);
        
        curImg++;
        if (curImg > maxImg) curImg = 1;
    }, 5000);
}

/*
    Setup events on page and start slideshow.
*/
window.onload = function() {
    setUpGlobals();

    main = document.getElementsByTagName("main")[0];
    transition_div = document.querySelector(".transition");
    logo = document.getElementById("logo");

    slideshow();
}
