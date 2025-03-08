document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("start").addEventListener("click", () => {
        fetch("http://localhost:5000/start")
            .then(response => response.text())
            .then(data => console.log(data));
    });

    document.getElementById("stop").addEventListener("click", () => {
        fetch("http://localhost:5000/stop")
            .then(response => response.text())
            .then(data => console.log(data));
    });
});
