
function checkReload() {
    fetch("/needs-update")
        .then(res => res.json())
        .then((res) => {
            if(res === true) {
                location.reload();
            }
        })
}


window.addEventListener('load', () => {
    setInterval(checkReload, 500);
})