let recipe_desc, btn_fav;
let inp_comment, btn_post_comment, btn_edit_comment, inp_edit_comment, btn_remove_comment, comment_section;
let btns_upvote, btns_downvote;

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

/*
    Remove a recipe from users favourites.
*/
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

/*
    Toggle if the favourite icon to represent the users choice.
*/
function toggle_favourite() {
    let favourite = btn_fav.getAttribute("data-fav");
    btn_fav.src = favourite == "false" ? "/static/images/fav-on.svg" : "/static/images/fav-off.svg";
    btn_fav.setAttribute("data-fav", favourite == "false" ? "true" : "false");
}

/*
    Creates a new comment object to be added.
*/
function create_new_comment(users_comment) {
    var comment_wrapper = document.createElement("div");
    comment_wrapper.className = "comment-wrapper";

    var comment = document.createElement("div");
    comment.className = "comment";

    var comment_details = document.createElement("div");
    comment_details.className = "comment-details";

    var new_comment = document.createElement("input");
    new_comment.type = "text";
    new_comment.disabled = true;
    new_comment.name = "users_comment";
    new_comment.value = users_comment;
    inp_edit_comment = new_comment;

    var account_link = document.createElement("a");
    account_link.href = `/account/${getCookie("user")}`;
    account_link.innerText = getCookie("user");

    var new_comment_date = document.createElement("span");
    new_comment_date.innerText = "Just Now";

    comment_details.appendChild(new_comment);
    comment_details.appendChild(account_link);
    comment_details.appendChild(new_comment_date);

    var comment_rating = document.createElement("div");
    comment_rating.className = "comment-rating";

    var upvote = document.createElement("img")
    upvote.src = "/static/images/vote.svg";
    upvote.className = "upvote";

    var rating = document.createElement("span");
    rating.innerText = "0";

    var downvote = document.createElement("img");
    downvote.src = "/static/images/vote.svg";
    downvote.className = "downvote";

    comment_rating.appendChild(upvote);
    comment_rating.appendChild(rating);
    comment_rating.appendChild(downvote);

    var comment_actions = document.createElement("div");
    comment_actions.className = "comment-actions";

    var btn_edit = document.createElement("button")
    btn_edit.type = "button";
    btn_edit.id = "btn-edit-comment";
    btn_edit.setAttribute("data-edit", "true");
    btn_edit.innerText = "Edit";
    btn_edit_comment = btn_edit;

    btn_edit.addEventListener("click", function () { edit_comment(); });

    var btn_delete = document.createElement("button");
    btn_delete.type = "button";
    btn_delete.id = "btn-remove-comment";
    btn_delete.innerText = "Delete";

    btn_delete.addEventListener("click", function () { remove_comment(this); });

    comment_actions.appendChild(btn_edit);
    comment_actions.appendChild(btn_delete);

    comment.appendChild(comment_details);
    comment.appendChild(comment_rating);

    comment_wrapper.appendChild(comment);
    comment_wrapper.appendChild(comment_actions);
    return comment_wrapper;
}

/*
    Add a new comment for a user.
*/
function add_comment() {
    var comment = inp_comment.value;

    if (comment != "") {
        var currentPage = window.location.href;
        var http = new XMLHttpRequest();
        http.open("GET", `${currentPage}/addcomment?comment=${comment}`, true);
        http.onreadystatechange = function () {
            if (http.readyState == 4 && http.status == 200 && http.responseText == "Y") {
                new_comment_tile = create_new_comment(comment);
                comment_section.appendChild(new_comment_tile);
            }
        }
        http.send();
    }
}

/*
    Remove an existing comment for a user.
*/
function remove_comment(btn) {
    var p = btn.parentElement;
    var pp = p.parentElement;
    var ppp = pp.parentElement;

    var currentPage = window.location.href;
    var http = new XMLHttpRequest();
    http.open("GET", `${currentPage}/removecomment`, true)
    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200 && http.responseText == "Y") ppp.removeChild(pp);
    }
    http.send();
}

/*
    Update GUI to show users new comment change.
*/
function edit_comment() {
    if (btn_edit_comment.getAttribute("data-edit") == "true") {
        inp_edit_comment.disabled = false;
        inp_edit_comment.focus();
        btn_edit_comment.innerText = "Save";
        btn_edit_comment.setAttribute("data-edit", "false");
    } else {
        inp_edit_comment.disabled = true;
        btn_edit_comment.innerText = "Edit";
        btn_edit_comment.setAttribute("data-edit", "true");
        save_edit(inp_edit_comment.value);
    }
}

/* 
    Save the users edit they made to a comment.
*/
function save_edit(comment) {
    if (comment != null) { 
        var currentPage = window.location.href;
        var http = new XMLHttpRequest();
        http.open("GET", `${currentPage}/editcomment?comment=${comment}`);
        http.onreadystatechange = function () {
            if (http.readyState == 4 && http.status == 200 && http.responseText == "Y") inp_edit_comment.value = comment;
        }
        http.send();
    }
}

/*
    Add a comment rating for a comment.
*/
function add_vote(obj, vote) {
    var target = `${window.location.href}/addrating?cid=${obj.parentElement.parentElement.getAttribute("data-id")}&r=${vote}`;
    var http = new XMLHttpRequest();
    http.open("GET", target, true);
    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200 && http.responseText != "N") {
            set_comment_rating_buttons(obj, vote, Number(http.responseText));
        }
    }
    http.send();
}

/* 
    Change GUI to reflect users rating change.
*/
function set_comment_rating_buttons(obj, vote, response) {
    var parent = obj.parentElement;
    var other_obj = vote == 1 ? parent.querySelector(".downvote") : parent.querySelector(".upvote");
    var rating = parent.querySelector("span");

    if (response == 0) {
        obj.src = "/static/images/vote.svg";
        rating.innerText = vote == 1 ? Number(rating.innerText) - 1 : Number(rating.innerText) + 1;
    } else if (response == 1 || response == -1) {
        obj.src = "/static/images/voted.svg";
        other_obj.src = "/static/images/vote.svg";
        rating.innerText = vote == 1 ? Number(rating.innerText) + 1 : Number(rating.innerText) - 1;
    }
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
    inp_comment = document.getElementById("inp-comment");
    btn_post_comment = document.getElementById("btn-post");
    btn_edit_comment = document.getElementById("btn-edit-comment");
    btn_remove_comment = document.getElementById("btn-remove-comment");
    inp_edit_comment = document.querySelector("input[name='users_comment']");
    comment_section = document.getElementById("comment-section");
    btns_upvote = document.getElementsByClassName("upvote");
    btns_downvote = document.getElementsByClassName("downvote");

    if (btn_fav != null) btn_fav.addEventListener("click", function () { 
        if (this.getAttribute("data-fav") == "false") add_favourite(recipe_id);
        else delete_favourite(recipe_id); 
    });

    if (btn_edit_comment != null) {
        btn_edit_comment.addEventListener("click", function () { edit_comment(); });
        btn_remove_comment.addEventListener("click", function () { remove_comment(this); });
    }

    btn_post_comment.addEventListener("click", function () { add_comment(); });

    for (var i = 0; i < btns_downvote.length; i++) {
        btns_downvote[i].addEventListener("click", function () { add_vote(this, -1); });
        btns_upvote[i].addEventListener("click", function () { add_vote(this, 1); });        
    }

    fadeIn();
}