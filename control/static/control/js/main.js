
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("menu-toggle");
    const overlay = document.getElementById("sidebar-overlay");

    if (!sidebar || !toggleBtn) {
        return;
    }

    const icon = toggleBtn.querySelector("i");


    

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");

        if (overlay) {
            overlay.classList.toggle("active");
        }

        if (icon) {
            icon.classList.toggle("fa-bars");
            icon.classList.toggle("fa-xmark");
        }
    });


    

    if (overlay) {
        overlay.addEventListener("click", () => {
            closeSidebar();
        });
    }


    

    const sidebarLinks =
        document.querySelectorAll(".sidebar-link");

    sidebarLinks.forEach(link => {
        link.addEventListener("click", () => {

            if (window.innerWidth <= 900) {
                closeSidebar();
            }

        });
    });


    

    const currentPath =
        window.location.pathname.replace(/\/+$/, "");

    sidebarLinks.forEach(link => {

        const linkPath =
            new URL(link.href, window.location.origin)
                .pathname
                .replace(/\/+$/, "");

        if (
            linkPath === currentPath ||
            (
                linkPath !== "" &&
                currentPath.startsWith(linkPath + "/")
            )
        ) {
            link.classList.add("active");
        }

    });


    

    function closeSidebar() {

        sidebar.classList.remove("open");

        if (overlay) {
            overlay.classList.remove("active");
        }

        if (icon) {
            icon.classList.remove("fa-xmark");
            icon.classList.add("fa-bars");
        }
    }


    

    window.addEventListener("resize", () => {

        if (window.innerWidth > 900) {
            closeSidebar();
        }

    });

});

