document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.getElementById("hamburger-menu");
    const navMenu = document.querySelector("nav ul");

    hamburger.addEventListener("click", function () {
        navMenu.classList.toggle("show");
    });
});

// Theme toggle
const themeToggle = document.getElementById("toggle-theme");
themeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    themeToggle.textContent = document.body.classList.contains("dark-mode")
        ? "Switch to Light Mode"
        : "Switch to Dark Mode";
});
