
document.addEventListener("DOMContentLoaded", function () {
    const referralInput = document.getElementById("referralLink");
    const copyButton = document.getElementById("copyReferralBtn");
    const copyMessage = document.getElementById("copyMessage");

    if (referralInput && copyButton) {

        copyButton.addEventListener("click", async function () {

            const referralLink = referralInput.value;

            try {

                
                await navigator.clipboard.writeText(referralLink);

            } catch (error) {

                

                referralInput.select();
                referralInput.setSelectionRange(0, 99999);

                document.execCommand("copy");

                window.getSelection().removeAllRanges();
            }

            

            const originalContent = copyButton.innerHTML;

            copyButton.innerHTML =
                '<i class="fas fa-check"></i><span>Copied!</span>';

            if (copyMessage) {
                copyMessage.textContent = "Referral link copied successfully.";
            }

            

            setTimeout(function () {

                copyButton.innerHTML = originalContent;

                if (copyMessage) {
                    copyMessage.textContent = "";
                }

            }, 2000);

        });

    }


    

    const chartCanvas = document.getElementById("referralChart");

    if (chartCanvas && typeof Chart !== "undefined") {

        const ctx = chartCanvas.getContext("2d");

        const referralElement =
            document.querySelector(
                ".referral-stats .stat-item:nth-child(1) strong"
            );

        const earningsElement =
            document.querySelector(
                ".referral-stats .stat-item:nth-child(2) strong"
            );

        const totalReferrals = referralElement
            ? parseInt(referralElement.innerText.replace(/,/g, "")) || 0
            : 0;

        const totalEarnings = earningsElement
            ? parseFloat(
                earningsElement.innerText
                    .replace("$", "")
                    .replace(/,/g, "")
            ) || 0
            : 0;


        new Chart(ctx, {

            type: "bar",

            data: {

                labels: [
                    "Total Referrals",
                    "Total Earnings"
                ],

                datasets: [{

                    label: "Referral Performance",

                    data: [
                        totalReferrals,
                        totalEarnings
                    ],

                    backgroundColor: [
                        "#4CAF50",
                        "#2196F3"
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
                        display: false
                    },

                    tooltip: {
                        enabled: true
                    }

                },

                scales: {

                    y: {
                        beginAtZero: true,

                        ticks: {
                            color: "#ffffff"
                        },

                        grid: {
                            color: "rgba(255,255,255,.08)"
                        }
                    },

                    x: {

                        ticks: {
                            color: "#ffffff"
                        },

                        grid: {
                            display: false
                        }

                    }

                }

            }

        });

    }

});

