let userField, passField1, passField2;
let btnSignup;
let inputs;

function enableButton() {
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].getAttribute("data-valid") == "false") {
            btnSignup.disabled = true;
            return;
        }
    }

    btnSignup.disabled = false;
}

function checkUsernameLength() {
    if (userField.value.length > 5) {
        userField.className = "border-suc";
        userField.setAttribute("data-valid", "true");
    } else {
        userField.className = "border-fail";
        userField.setAttribute("data-valid", "false");
    }

    enableButton();
}

function checkPasswordStrength() {
    let str = passField1.value;
    if (str.includes("£") || str.includes("!") || str.includes("?") || str.includes("$") ||
        str.includes("#") || str.includes("_") || str.includes("-") || str.includes("+") ||
        str.includes("=") || str.includes("~")) {
            if (str.match(".*?([0-9]).*?").length != null && str.length > 8) {
                passField1.className = "border-suc";
                passField1.setAttribute("data-valid", "true");
            }
        }
    else {
        passField1.className = "border-fail";
        passField1.setAttribute("data-valid", "false");
    }

    enableButton();
}

function checkPasswordMatches() {
    if (passField1.value == passField2.value) {
        passField2.className = "border-suc";
        passField2.setAttribute("data-valid", "true");
    } else {
        passField2.className = "border-fail";
        passField2.setAttribute("data-valid", "false");
    }

    enableButton();
}

window.onload = function() {
    setUpGlobals();

    userField = document.querySelector('input[name="username"]');
    passField1 = document.querySelector('input[name="password"]');
    passField2 = document.querySelector('input[name="confPassword"]');
    btnSignup = document.querySelector("button");
    inputs = document.getElementsByTagName("input");

    userField.addEventListener("input", function () { checkUsernameLength(); });
    passField1.addEventListener("input", function () { checkPasswordStrength(); }); 
    passField2.addEventListener("input", function () { checkPasswordMatches() });
}