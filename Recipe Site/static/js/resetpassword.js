let inp_email, btn_send_email, email_sent_div;
let inp_code, inp_new_pass, inp_new_pass_conf, btn_reset;

function enableButton() {
    if (inp_new_pass.getAttribute("data-valid") == "true" && inp_new_pass_conf.getAttribute("data-valid") == "true") {
        btn_reset.disabled = false;
    } else {
        btn_reset.disabled = true;
    }
}

/*
    Check password has a special character and a number in it.
*/
function checkPasswordStrength() {
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

    enableButton();
}

/*
    Check that both inputted passwords match.
*/
function checkPasswordMatches() {
    if (inp_new_pass.value == inp_new_pass_conf.value) {
        inp_new_pass_conf.className = "border-suc";
        inp_new_pass_conf.setAttribute("data-valid", "true");
    } else {
        inp_new_pass_conf.className = "border-fail";
        inp_new_pass_conf.setAttribute("data-valid", "false");
    }

    enableButton();
}

/*
    Sends a request for an email to be sent to specified address.
*/
function send_email() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        }
    };

    xhttp.open("GET", `/resetpassword?email=${inp_email.value}`, true);
    xhttp.send();
}

window.onload = function () {
    setUpGlobals();

    inp_email = document.querySelector("form input");
    btn_send_email = document.querySelector("button");
    email_sent_div = document.querySelector(".email-sent");
    inp_code = document.querySelector("input[name='code']");
    inp_new_pass = document.querySelector("input[name='pass']");
    inp_new_pass_conf = document.querySelector("input[name='pass_conf']");
    btn_reset = document.getElementById("btn_reset");

    if (btn_send_email != null) {
            btn_send_email.addEventListener("click", function () {
            send_email();
            email_sent_div.style.opacity = "1";
        });
    }

    if (inp_new_pass != null) inp_new_pass.addEventListener("input", function () { checkPasswordStrength(); });
    if (inp_new_pass_conf != null) inp_new_pass_conf.addEventListener("input", function () { checkPasswordMatches(); });
}