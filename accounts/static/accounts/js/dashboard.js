
document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebar-overlay");

    if (!menuToggle || !sidebar) {
        return;
    }

    const menuIcon = menuToggle.querySelector("i");

    function openSidebar() {
        sidebar.classList.add("active");

        if (sidebarOverlay) {
            sidebarOverlay.classList.add("active");
        }

        menuToggle.classList.add("active");
        menuToggle.setAttribute("aria-expanded", "true");
        menuToggle.setAttribute("aria-label", "Close menu");

        menuIcon.classList.remove("fa-bars");
        menuIcon.classList.add("fa-xmark");

        document.body.classList.add("sidebar-open");
    }

    function closeSidebar() {
        sidebar.classList.remove("active");

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("active");
        }

        menuToggle.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Open menu");

        menuIcon.classList.remove("fa-xmark");
        menuIcon.classList.add("fa-bars");

        document.body.classList.remove("sidebar-open");
    }

    menuToggle.addEventListener("click", function () {

        if (sidebar.classList.contains("active")) {
            closeSidebar();
        } else {
            openSidebar();
        }

    });

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", function () {
            closeSidebar();
        });
    }

    const menuLinks = sidebar.querySelectorAll(".menu-link");

    menuLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            closeSidebar();
        });
    });

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {
            closeSidebar();
        }

    });

});


document.addEventListener("DOMContentLoaded", function () {
const copyButton = document.getElementById("copy-referral-btn");
const referralInput = document.getElementById("referral-link");

if (!copyButton || !referralInput) {
    return;
}

copyButton.addEventListener("click", function () {
    const referralLink = referralInput.value;

    navigator.clipboard.writeText(referralLink)
        .then(function () {
            const originalContent = copyButton.innerHTML;

            copyButton.innerHTML =
                '<i class="fa-solid fa-check"></i><span>Copied!</span>';

            copyButton.classList.add("copied");

            setTimeout(function () {
                copyButton.innerHTML = originalContent;
                copyButton.classList.remove("copied");
            }, 2000);
        })
        .catch(function () {
            referralInput.select();
            referralInput.setSelectionRange(0, 99999);

            document.execCommand("copy");

            const originalContent = copyButton.innerHTML;

            copyButton.innerHTML =
                '<i class="fa-solid fa-check"></i><span>Copied!</span>';

            copyButton.classList.add("copied");

            setTimeout(function () {
                copyButton.innerHTML = originalContent;
                copyButton.classList.remove("copied");
            }, 2000);
        });
});


});

document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("performanceChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    const performanceChart = new Chart(ctx, {
        type: "bar",

        data: {
            labels: [],

            datasets: [{
                label: "Balances",
                data: [],

                backgroundColor: [
                    "#FFD700",
                    "#6793e3"
                ],

                borderRadius: 8,
                borderWidth: 0
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff",
                        font: {
                            size: 13,
                            weight: "bold"
                        }
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: "#ffffff",
                        font: {
                            size: 12,
                            weight: "600"
                        }
                    },

                    grid: {
                        color: "rgba(255, 255, 255, 0.08)",
                        drawBorder: false
                    }
                },

                y: {
                    beginAtZero: true,

                    ticks: {
                        color: "#ffffff",
                        font: {
                            size: 12,
                            weight: "600"
                        }
                    },

                    grid: {
                        color: "rgba(255, 255, 255, 0.08)",
                        drawBorder: false
                    }
                }
            }
        }
    });

    function updateChart() {
        fetch("/accounts/performance-data/")
            .then(response => response.json())
            .then(data => {
                performanceChart.data.labels = data.labels;
                performanceChart.data.datasets[0].data = data.values;

                performanceChart.update();
            })
            .catch(err => {
                console.error("Chart update failed:", err);
            });
    }

    updateChart();
    setInterval(updateChart, 10000);
});

