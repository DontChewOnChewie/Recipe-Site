let btn_change_pass, btn_email_auth;
let inp_cur_pas, inp_new_pass, inp_new_pass_conf, inp_email, inp_email_pass;
let delete_account_check, btn_delete_account, btn_yes, btn_no;

/*
    Code here very similar to that of signup.js basically just making sure that the new password is
    strong enough before allowing the user to change it.
*/

function enable_password_button(btn) {
    let password_inputs = document.getElementById("change_password").getElementsByTagName("input");
    
    for (var i = 0; i < password_inputs.length; i++) {
        if (password_inputs[i].getAttribute("data-valid") == "false") {
            btn_change_pass.disabled = true;
            return;
        }
    }

    btn_change_pass.disabled = false;
}

function check_cur_password() {
    if (inp_cur_pas.value.length > 8) {
        inp_cur_pas.className = "border-suc";
        inp_cur_pas.setAttribute("data-valid", "true");
    } else {
        inp_cur_pas.className = "border-fail";
        inp_cur_pas.setAttribute("data-valid", "false");
    }
}

function check_new_password() {
    let str = inp_new_pass.value;
    if (str.includes("£") || str.includes("!") || str.includes("?") || str.includes("$") ||
        str.includes("#") || str.includes("_") || str.includes("-") || str.includes("+") ||
        str.includes("=") || str.includes("~")) {
            if (str.match(".*?([0-9]).*?").length != null && str.length > 8) {
                inp_new_pass.className = "border-suc";
                inp_new_pass.setAttribute("data-valid", "true");
            }
        }
    else {
        inp_new_pass.className = "border-fail";
        inp_new_pass.setAttribute("data-valid", "false");
    }

    enable_password_button();
}

function check_new_password_mathces() {
    if (inp_new_pass.value == inp_new_pass_conf.value) {
        inp_new_pass_conf.className = "border-suc";
        inp_new_pass_conf.setAttribute("data-valid", "true");
    } else {
        inp_new_pass_conf.className = "border-fail";
        inp_new_pass_conf.setAttribute("data-valid", "false");
    }

    enable_password_button();
}

/*
    Check that email has an @ and a . in it. Could look into better regex for this.
*/
function check_email() {
    if (inp_email.value != "" && inp_email.value.indexOf("@") != -1 && inp_email.value.indexOf(".") != -1) {
        inp_email.className = "border-suc";
        btn_email_auth.disabled = false;
    } else {
        inp_email.className = "border-fail";
        btn_email_auth.disabled = true;
    }
}

function fade_delete_account(opacity) {
    delete_account_check.style.opacity = opacity;
}

window.onload = function() {
    setUpGlobals();

    btn_change_pass = document.getElementById("btn_change_password");
    btn_email_auth = document.getElementById("btn_email_auth");
    inp_cur_pas = document.querySelector("input[name='current_pass']");
    inp_new_pass = document.querySelector("input[name='new_pass']");
    inp_new_pass_conf = document.querySelector("input[name='new_pass_conf']");
    inp_email = document.querySelector("input[name='email']");
    inp_email_pass = document.querySelector("input[name='email_pass']");
    btn_delete_account = document.querySelector("#delete_account button")
    delete_account_check = document.querySelector(".delete_account_check");
    btn_no = document.getElementById("no");
    btn_yes = document.getElementById("yes");

    if (inp_cur_pas != null) {
        inp_cur_pas.addEventListener("input", function () { check_cur_password(); });
        inp_new_pass.addEventListener("input", function () { check_new_password(); });
        inp_new_pass_conf.addEventListener("input", function () { check_new_password_mathces(); });
        inp_email.addEventListener("input", function () { check_email(); });
        btn_delete_account.addEventListener("click", function () { fade_delete_account(1); });
        btn_no.addEventListener("click", function () { fade_delete_account(0); });
        btn_yes.addEventListener("click", function () { window.location = `/account/${getCookie("user")}/delete` });
    }
}