let curImg = 1;
let maxImg = 4;
let main, transition_div, sign_in_wrapper, btn_login, logo;

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

function animateLogInForm() {
    sign_in_wrapper.className = "sign-in-wrapper sign-in-wrapper-active";
    setTimeout(function() {
        sign_in_wrapper.className="sign-in-wrapper";
    }, 1200)
}

window.onload = function() {
    setUpGlobals();

    main = document.getElementsByTagName("main")[0];
    transition_div = document.querySelector(".transition");
    sign_in_wrapper = document.querySelector(".sign-in-wrapper");
    btn_login = document.querySelector("a[href='#']");
    logo = document.getElementById("logo");

    if (btn_login != null) btn_login.addEventListener("click", function() { animateLogInForm(); });
    logo.addEventListener("click", function() { window.location = "/"; });
    slideshow();
}
