function getDiff() {
    // Flask (and all WSGI servers) decode strings by default, so any branch name
    // with a slash in it will be interpreted as path params. A hacky way out is
    // to double encode the URI component.
    const head = encodeURIComponent(encodeURIComponent("feature/frontend"));
    fetch(`http://localhost:8080/diff/base/${head}`, {
        method: 'GET'
    }).then(
        function(response) {
            if (response.ok) {
                response.text().then((text) => {
                    document.body.innerHTML = text;
                })
            }
        })
}

getDiff()