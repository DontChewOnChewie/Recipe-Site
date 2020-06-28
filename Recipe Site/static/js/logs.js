let parent;
let sel_type, sel_status, inp_url, inp_ip, inp_user_agent;
let current_params = {"type" : "", "status" : "", "url" : "", "ip" : "", "user-agent" : ""};

let mouseX, mouseY;

function filter(obj) {
    var keys = Object.keys(current_params);
    var http = new XMLHttpRequest();
    var params = "";

    current_params[obj.id] = obj.value;
    for (var i = 0; i < keys.length; i++) {
        params += i == 0 ? `${keys[i]}=${current_params[keys[i]]}` : `&${keys[i]}=${current_params[keys[i]]}`;
    }

    http.open("GET", `/logs/filter?${params}`, true);
    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200 && http.responseText != "N") {
            var t = document.querySelector("table");
            var tb = document.querySelector("tbody");
            var rows = t.querySelectorAll("tr").length;
            for (var i = 0; i < rows - 1; i++) {
                t.deleteRow(1);
            }
            
            tb.innerHTML = tb.innerHTML + http.responseText;
            setup_td_events();
        }
    }
    http.send();
}

function setup_td_events() {
    var cells = document.getElementsByTagName("td");
    for (var i = 0; i < cells.length; i++) {
        cells[i].addEventListener("dblclick", function () { show_td_popup(this); });
    }
}

function show_td_popup(obj) {
    var mouseX = event.clientX;
    var popup_wrapper = document.createElement("div");
    var popup_message = document.createElement("div");
    var popup_close = document.createElement("div");

    popup_wrapper.style.left = mouseX  + parent.scrollLeft + "px";
    popup_wrapper.style.top = mouseY - 100 + "px";
    popup_wrapper.className = "popup-wrapper";

    popup_message.className = "popup";
    popup_message.innerText = obj.innerText;

    popup_close.className = "popup-close";
    popup_close.addEventListener("click", function () {
        parent.removeChild(popup_wrapper);
    });

    popup_wrapper.appendChild(popup_close);
    popup_wrapper.appendChild(popup_message);

    parent.appendChild(popup_wrapper);
}

window.onload = function () {
    setUpGlobals();
    
    parent = document.querySelector(".content-pain");
    sel_type = document.getElementById("type");
    sel_status = document.getElementById("status");
    inp_url = document.getElementById("url");
    inp_ip = document.getElementById("ip");
    inp_user_agent = document.getElementById("user-agent");

    sel_type.addEventListener("change", function () { filter(this); });
    sel_status.addEventListener("change", function () { filter(this); });
    inp_url.addEventListener("input", function () { filter(this) });
    inp_ip.addEventListener("input", function () { filter(this); });
    inp_user_agent.addEventListener("input", function () { filter(this); });
    parent.addEventListener("mousemove", function (event) {
        mouseX = event.clientX;
        mouseY = event.clientY;
    });
    setup_td_events();
}