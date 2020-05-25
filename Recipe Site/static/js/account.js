let recipes, delete_btns, add_btn, add_recipe_div, modal, modal_close_btn;

function deleteRecipe(recipeBtn) {
    let pp = recipeBtn.parentNode.parentNode;
    let p = recipeBtn.parentNode

    let link = p.getElementsByClassName("recipe-details")[0].getAttribute("href");

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        }
    };

    xhttp.open("DELETE", `${link}/delete`, true);
    xhttp.send();
    
    pp.removeChild(p);
}

function addRecipe() {
    let recipe_name = document.querySelector("input[name='name']").value;
    let recipe_desc = document.querySelector("input[name='desc']").value;
    let recipe_creator = getCookie("user");

    var http = new XMLHttpRequest();
    var params = `name=${recipe_name}&desc=${recipe_desc}&creator=${recipe_creator}`;
    http.open('PUT', `http://localhost:5000/account/${recipe_creator}/${recipe_name}/add?${params}`, true);

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
        }
    }
    http.send();
}

function openModal() {
    modal.style.display = "flex";
    setTimeout(() => {
        modal.style.opacity = "1";
    }, 200);
}

function closeModal() {
    modal.style.opacity = "0";
    setTimeout(() => {
        modal.style.display = "none";
    }, 600);
}

window.onload = function () {
    setUpGlobals();

    recipes = document.getElementsByClassName("recipe-details");
    delete_btns = document.getElementsByClassName("delete-btn");
    add_btn = document.getElementById("add-btn");
    add_recipe_div = document.getElementById("add-recipe-btn")
    modal = document.querySelector(".modal");
    modal_close_btn = document.querySelector(".modal p");
    
    for (var i = 0; i < recipes.length; i++) {
        recipes[i].addEventListener("click", function () { window.location = this.getAttribute("href"); });
        delete_btns[i].addEventListener("click", function () { deleteRecipe(this); });
    }

    add_btn.addEventListener("click", function () { addRecipe(); });
    add_recipe_div.addEventListener("click", function () { openModal(); });
    modal_close_btn.addEventListener("click", function () { closeModal(); });
}