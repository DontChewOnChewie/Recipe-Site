let recipes, delete_btns, add_btn, add_recipe_div, modal, modal_close_btn, form_add, add_ingr_btn;

/*
    Makes an XHR request to the delete recipe page and removes the recipe
    if the server returns 'Y'
*/
function deleteRecipe(recipeBtn) {
    let pp = recipeBtn.parentNode.parentNode;
    let p = recipeBtn.parentNode

    let link = p.getElementsByClassName("recipe-details")[0].getAttribute("href");

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "Y") pp.removeChild(p);
        }
    };

    xhttp.open("DELETE", `${link}/delete`, true);
    xhttp.send();
}

/*
    Returns a JSON string of all the recipes the user wants to add to a recipe.
*/
function getIngredients() {
    let ingrParents = document.getElementsByClassName("ingredient-wrapper");

    let optional = {}
    let needed = {}
    let return_json = {};

    for (var i = 0; i < ingrParents.length; i++) {
        let ing = ingrParents[i].getElementsByTagName("input")[0].value;
        let amt = ingrParents[i].getElementsByTagName("input")[1].value;
        let opt = ingrParents[i].getElementsByTagName("input")[2].checked;

        if (ing == "" || amt == "") continue;

        if (opt) optional[ing] = amt;
        else needed[ing] = amt;
    }

    return_json["needed"] = needed;
    return_json["optional"] = optional;
    return JSON.stringify(return_json);
}

/*
    New lines would not be put into database so instead they are replaced with random
    characters for DB storage and then formatted when the page loads.
*/
function format_recipe_description_for_db(desc) {
    let res = desc;
    while (res.indexOf("\n") != -1) {
        res = res.replace("\n", "$?");
    }
    return res;
} 

/*
    Format recipe description to include new lines.
*/
function format_recipe_description_for_web() {
    let descs = document.getElementsByClassName("description");
    for (var i = 0; i < descs.length; i++) {
        let new_desc = descs[i].innerText;
        while (new_desc.indexOf("$?") != -1) {
            new_desc = new_desc.replace("$?", " ");
        }
        descs[i].innerText = new_desc;
    }
} 

/*
    Adds a recipe though XHR with users given arguments.
    Could display alert on success, or add new recipe to page.
*/
function addRecipe() {
    let recipe_name = document.querySelector("input[name='name']").value;
    let recipe_desc = document.querySelector("textarea").value;
    let all_ingerdients = getIngredients();
    let recipe_creator = getCookie("user");

    var http = new XMLHttpRequest();
    var params = `name=${recipe_name}&desc=${format_recipe_description_for_db(recipe_desc)}&creator=${recipe_creator}&ingredients=${all_ingerdients}`;
    http.open('PUT', `http://localhost:5000/account/${recipe_creator}/${recipe_name}/add?${params}`, true);

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
        }
    }
    http.send();
}

/* 
    Open modal to add a new recipe.
*/
function openModal() {
    modal.style.display = "flex";
    setTimeout(() => {
        modal.style.opacity = "1";
    }, 200);
}

/*
    Close modal and form for adding a new recipe.
*/
function closeModal() {
    modal.style.opacity = "0";
    setTimeout(() => {
        modal.style.display = "none";
    }, 600);
}

/*
    Adds new ingredient field to the form.
*/
function addNewIngredientField() {
    let div = document.createElement("div");
    div.className = "ingredient-wrapper";

    let ingInp = document.createElement("input");
    ingInp.placeholder = "Ingredient...";

    let amtInp = document.createElement("input");
    amtInp.placeholder = "Amount...";

    let lbl = document.createElement("label");
    lbl.innerText = "Optional";

    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";

    let btn = document.createElement("button");
    btn.innerText = "+";
    btn.type = "button";
    btn.addEventListener("click", function () { addNewIngredientField(); });

    div.appendChild(ingInp);
    div.appendChild(amtInp);
    div.appendChild(lbl);
    div.appendChild(checkbox);
    div.appendChild(btn);
    form_add.insertBefore(div, form_add.children[form_add.children.length - 1]);
}

/*
    Setup events for page and format recipe descriptions.
*/
window.onload = function () {
    setUpGlobals();

    recipes = document.getElementsByClassName("recipe-details");
    delete_btns = document.getElementsByClassName("delete-btn");
    add_btn = document.getElementById("add-btn");
    add_recipe_div = document.getElementById("add-recipe-btn")
    modal = document.querySelector(".modal");
    modal_close_btn = document.querySelector(".modal p");
    form_add = document.querySelector("form");
    add_ingr_btn = document.querySelector(".ingredient-wrapper button");
    
    for (var i = 0; i < recipes.length; i++) {
        recipes[i].addEventListener("click", function () { window.location = this.getAttribute("href"); });
        if (delete_btns.length > 0) delete_btns[i].addEventListener("click", function () { deleteRecipe(this); });
    }

    add_btn.addEventListener("click", function () { addRecipe(); });
    if (add_recipe_div != null) add_recipe_div.addEventListener("click", function () { openModal(); });
    modal_close_btn.addEventListener("click", function () { closeModal(); });
    add_ingr_btn.addEventListener("click", function () { addNewIngredientField(); });

    format_recipe_description_for_web();
}