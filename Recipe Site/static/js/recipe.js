let recipe_desc;

/*
    Fade in page so that the description can be foramtted.
*/
function fadeIn() {
    let target = document.querySelector("main");

    setTimeout(() => {
        target.style.opacity = "1";
    }, 300);
}

/*
    Format description to include new lines.
*/
function format_recipe_description_for_web(desc) {
    let res = desc;
    while (res.indexOf("$?") != -1) {
        res = res.replace("$?", "<br/>");
    }
    return res;
} 

/*
    Setup page events and fade in content.
*/
window.onload = function() {
    setUpGlobals();

    recipe_desc = document.querySelector(".content-pain, p");
    recipe_desc.innerHTML = this.format_recipe_description_for_web(recipe_desc.innerHTML);
    fadeIn();
}