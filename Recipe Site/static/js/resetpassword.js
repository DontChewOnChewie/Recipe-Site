let inp_email, btn_send_email, email_sent_div;
let inp_code;

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
    addURLCode();

    inp_email = document.querySelector("form input");
    btn_send_email = document.querySelector("button");
    email_sent_div = document.querySelector(".email-sent");
    inp_code = document.querySelector("input[name='code']")

    if (btn_send_email != null) {
            btn_send_email.addEventListener("click", function () {
            send_email();
            email_sent_div.style.opacity = "1";
        });
    }

    if (inp_code != null) {
        inp_code.value = inp_code.value;
    }
}