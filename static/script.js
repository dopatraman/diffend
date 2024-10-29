function showSpinner() {
    const el = document.getElementById('loading-screen')
    el.style.display = "flex";
}

function hideSpinner() {
    const el = document.getElementById('loading-screen')
    el.style.display = "none";
}

function getDiff() {
    showSpinner();
    // Flask (and all WSGI servers) decode strings by default, so any branch name
    // with a slash in it will be interpreted as path params. A hacky way out is
    // to double encode the URI component.
    const head = encodeURIComponent(encodeURIComponent("feature/frontend"));
    fetch(`http://localhost:8080/dopatraman/diffend/main/${head}`, {
        method: 'GET'
    }).then(
        function(response) {
            if (response.ok) {
                response.text().then((text) => {
                    hideSpinner();
                })
            }
        })
}

hideSpinner();