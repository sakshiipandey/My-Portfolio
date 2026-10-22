document.addEventListener("DOMContentLoaded", function () {

    // Mobile navigation
    const toggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (toggle && navLinks) {
        toggle.addEventListener("click", function () {
            navLinks.classList.toggle("open");
        });
    }

    // Automatic footer year
    const year = document.getElementById("current-year");

    if (year) {
        year.textContent = new Date().getFullYear();
    }

    // Admin dashboard: edit project
    const form = document.getElementById("project-form");

    if (!form) return;

    const cancelButton = document.getElementById("cancel-edit");

    document.querySelectorAll(".edit-project").forEach(function (button) {

        button.addEventListener("click", function () {

            document.getElementById("project_id").value =
                button.dataset.id;

            document.getElementById("title").value =
                button.dataset.title;

            document.getElementById("description").value =
                button.dataset.description;

            document.getElementById("tech").value =
                button.dataset.tech;

            document.getElementById("github_url").value =
                button.dataset.github;

            document.getElementById("live_url").value =
                button.dataset.live;

            document.getElementById("image_url").value =
                button.dataset.image;

            document.getElementById("featured").checked =
                button.dataset.featured === "1";

            document.getElementById("form-title").textContent =
                "Edit Project";

            document.getElementById("save-button").textContent =
                "Update Project";

            cancelButton.hidden = false;

            form.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });

    cancelButton.addEventListener("click", function () {

        form.reset();

        document.getElementById("project_id").value = "";

        document.getElementById("form-title").textContent =
            "Add New Project";

        document.getElementById("save-button").textContent =
            "Save Project";

        cancelButton.hidden = true;

    });

});