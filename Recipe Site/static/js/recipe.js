let recipe_desc, btn_fav;

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
    Add a recipe to users favourites;
*/
function add_favourite(recipe_id) {
    var currentPage = window.location.href;
    var http = new XMLHttpRequest();
    var params = `recipe=${recipe_id}`;
    http.open('PUT', `${currentPage}/favourites/add?${params}`, true);

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
        }

        console.log(this.responseText);
    }
    http.send();

    toggle_favourite();
}


function delete_favourite(recipe_id) {
    var currentPage = window.location.href;
    var http = new XMLHttpRequest();
    http.open('DELETE', `${currentPage}/favourites/delete/${recipe_id}`, true);

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
        }
    }
    http.send();

    toggle_favourite();
}

function toggle_favourite() {
    let favourite = btn_fav.getAttribute("data-fav");
    btn_fav.src = favourite == "false" ? "/static/images/fav-on.svg" : "/static/images/fav-off.svg";
    btn_fav.setAttribute("data-fav", favourite == "false" ? "true" : "false");
}

/*
    Setup page events and fade in content.
*/
window.onload = function() {
    setUpGlobals();

    recipe_desc = document.querySelector(".content-pain, p");
    recipe_desc.innerHTML = this.format_recipe_description_for_web(recipe_desc.innerHTML);
    let recipe_id = document.getElementById("id").innerText.split(":")[0];
    btn_fav = document.getElementById("favourite");
    if (btn_fav != null) btn_fav.addEventListener("click", function () { 
        if (this.getAttribute("data-fav") == "false") add_favourite(recipe_id);
        else delete_favourite(recipe_id); 
    });

    fadeIn();
}