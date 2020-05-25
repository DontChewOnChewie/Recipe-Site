let search, searchResults, logo;

function setUpGlobals() {
    search = document.getElementById("search");
    searchResults = document.getElementById("search-results")
    logo = document.getElementById("logo");

    search.addEventListener("mouseenter", function() { searchResults.style.display = "block"; });

    search.addEventListener("mouseleave", function () {searchResults.style.display = "none"; });

    search.addEventListener("input", function () { if (this.value.length > 0) getSearchResults(this.value); });

    searchResults.addEventListener("mouseover", function () { this.style.display = "block"; });
    
    searchResults.addEventListener("mouseout", function () { this.style.display = "none"; });

    logo.addEventListener("click", function () { window.location = "/"; });
}

function getSearchResults(searchTerm) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            searchResults.innerHTML = this.responseText;
        }
    };

    xhttp.open("GET", `http://localhost:5000/searchResult?s=${searchTerm}`, true);
    xhttp.send();
}

function createAlert(alert_title, alert_body, alert_type) {
    let wrapper = document.getElementById("wrapper");

    let alert = document.createElement("div");
    alert.className = `alert ${alert_type}`;

    let alertTitleWrapper = document.createElement("div");

    let alertCloseBtn = document.createElement("span");
    alertCloseBtn.innerText = "X";

    let alertTitle = document.createElement("h3");
    alertTitle.innerText = alert_title;

    alertTitleWrapper.appendChild(alertTitle);
    alertTitleWrapper.appendChild(alertCloseBtn);

    let alertBody = document.createElement("span");
    alertBody.innerText = alert_body;

    alert.appendChild(alertTitleWrapper);
    alert.appendChild(alertBody);

    alertCloseBtn.addEventListener("click", function () { closeAlert(); });

    wrapper.appendChild(alert);
}

function openAlert() {
    let alert = document.querySelector(".alert");
    alert.style.opacity = "1";
}

function closeAlert() {
    let alert = document.querySelector(".alert");
    alert.style.opacity = "0";

    setTimeout(function () {
        let parent = alert.parentElement;
        parent.removeChild(alert);
    }, 600); 
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
