

document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("bitcoinCanvas");

    if (!canvas) {
        return;
    }

    const displaySize = canvas.clientWidth || 300;

    canvas.width = displaySize;
    canvas.height = displaySize;

    const ctx = canvas.getContext("2d");

    if (!ctx) {
        return;
    }

    const img = new Image();

    img.src = "/static/core/images/bitcoin.jpg";

    let angle = 0;

    function draw() {

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        const radius = canvas.width / 2;

        ctx.save();

        ctx.translate(
            radius,
            radius
        );

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            radius,
            0,
            Math.PI * 2
        );

        ctx.clip();

        ctx.rotate(
            angle * Math.PI / 180
        );

        ctx.drawImage(
            img,
            -radius,
            -radius,
            canvas.width,
            canvas.height
        );

        ctx.restore();

        angle += 1;

        requestAnimationFrame(draw);
    }

    img.onload = draw;

});




function fetchCryptoStats() {

    fetch("/crypto-stats/")
        .then(function (response) {

            if (!response.ok) {
                throw new Error(
                    "Unable to fetch crypto statistics."
                );
            }

            return response.json();
        })
        .then(function (data) {

            const btcPrice =
                document.getElementById("btc-price");

            const ethPrice =
                document.getElementById("eth-price");

            const usdtErc20 =
                document.getElementById("usdt-erc20");

            const usdtTrc20 =
                document.getElementById("usdt-trc20");

            const btcVolume =
                document.getElementById("btc-volume");

            const activeTrades =
                document.getElementById("active-trades");


            if (btcPrice) {
                btcPrice.innerText =
                    `$${data.btc} USD`;
            }


            if (ethPrice) {
                ethPrice.innerText =
                    `$${data.eth} USD`;
            }


            if (usdtErc20) {
                usdtErc20.innerText =
                    `$${data.usdt} USD`;
            }


            if (usdtTrc20) {
                usdtTrc20.innerText =
                    `$${data.usdt} USD`;
            }


            if (btcVolume) {
                const volume =
                    Number(data.btc_volume) || 0;

                btcVolume.innerText =
                    `${volume.toLocaleString()} USD`;
            }


            if (activeTrades) {
                const trades =
                    Number(data.active_trades) || 0;

                activeTrades.innerText =
                    trades.toLocaleString();
            }

        })
        .catch(function (error) {

            console.error(
                "Crypto stats error:",
                error
            );

        });
}




fetchCryptoStats();

setInterval(
    fetchCryptoStats,
    10000
);




document.addEventListener("DOMContentLoaded", function () {

    const planSelect =
        document.getElementById("planSelect");

    const amountInput =
        document.getElementById("investAmount");

    const profitInput =
        document.getElementById("profitAmount");


    

    const resultInvestment =
        document.getElementById("resultInvestment");

    const resultRate =
        document.getElementById("resultRate");

    const resultProfit =
        document.getElementById("resultProfit");

    const resultTotal =
        document.getElementById("resultTotal");

    const resultFrequency =
        document.getElementById("resultFrequency");


    

    const calcError =
        document.getElementById("calcError");


    

    if (
        !planSelect ||
        !amountInput
    ) {
        return;
    }


    

    function extractNumber(value) {

        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {
            return 0;
        }

        const match =
            String(value).match(
                /-?\d+(?:\.\d+)?/
            );

        return match
            ? parseFloat(match[0])
            : 0;
    }


    

    function showError(message) {

        if (calcError) {

            calcError.textContent =
                message;

            calcError.classList.add(
                "show"
            );
        }

        amountInput.classList.add(
            "input-error"
        );
    }


    

    function clearError() {

        if (calcError) {

            calcError.textContent =
                "";

            calcError.classList.remove(
                "show"
            );
        }

        amountInput.classList.remove(
            "input-error"
        );
    }


    

    function resetCalculator() {

        clearError();


        if (profitInput) {
            profitInput.value = "";
        }


        if (resultInvestment) {

            resultInvestment.textContent =
                "$0.00";
        }


        if (resultRate) {

            resultRate.textContent =
                "0%";
        }


        if (resultProfit) {

            resultProfit.textContent =
                "$0.00";
        }


        if (resultTotal) {

            resultTotal.textContent =
                "$0.00";
        }


        if (resultFrequency) {

            resultFrequency.textContent =
                 resultFrequency.dataset.defaultText || "";
        }
    }


    

    function clearAmountResults() {

        clearError();


        if (profitInput) {
            profitInput.value = "";
        }


        if (resultInvestment) {

            resultInvestment.textContent =
                "$0.00";
        }


        if (resultRate) {

            resultRate.textContent =
                "0%";
        }


        if (resultProfit) {

            resultProfit.textContent =
                "$0.00";
        }


        if (resultTotal) {

            resultTotal.textContent =
                "$0.00";
        }


        if (resultFrequency) {

            resultFrequency.textContent =
                 resultFrequency.dataset.defaultText || "";
        }
    }


    

    function calculateProfit() {

        clearError();


        

        const option =
            planSelect.options[
                planSelect.selectedIndex
            ];


        

        if (
            !option ||
            !option.value
        ) {

            resetCalculator();

            return;
        }


        

        const amount =
            parseFloat(
                amountInput.value
            );


        

        if (
            isNaN(amount) ||
            amount <= 0
        ) {

            clearAmountResults();

            return;
        }


        

        const rateText =
            option.dataset.rate || "";

        const frequency =
            option.dataset.frequency || "";

        const periodsText =
            option.dataset.periods || "";

        const minimumText =
            option.dataset.min || "";

        const maximumText =
            option.dataset.max || "";


        

        const rate =
            extractNumber(rateText);

        const minimumInvestment =
            extractNumber(minimumText);

        const maximumInvestment =
            extractNumber(maximumText);

        let periods =
            extractNumber(periodsText);


        

        const isLifetime =
            String(periodsText)
                .toLowerCase()
                .includes("lifetime");


        if (isLifetime) {

            periods = 1;
        }


        

        if (resultInvestment) {

            resultInvestment.textContent =
                `$${amount.toFixed(2)}`;
        }


        

        if (resultRate) {

            resultRate.textContent =
                `${rate}%`;
        }


        

        if (
            minimumInvestment > 0 &&
            amount < minimumInvestment
        ) {

            showError(
                `Minimum investment for ${option.textContent.trim()} is $${minimumInvestment.toFixed(2)}.`
            );


            if (profitInput) {

                profitInput.value =
                    "";
            }


            if (resultProfit) {

                resultProfit.textContent =
                    "$0.00";
            }


            if (resultTotal) {

                resultTotal.textContent =
                    `$${amount.toFixed(2)}`;
            }


            if (resultFrequency) {

                resultFrequency.textContent =
                    `Minimum investment: $${minimumInvestment.toFixed(2)}`;
            }


            return;
        }


        

        if (
            maximumInvestment > 0 &&
            amount > maximumInvestment
        ) {

            showError(
                `Maximum investment for ${option.textContent.trim()} is $${maximumInvestment.toFixed(2)}.`
            );


            if (profitInput) {

                profitInput.value =
                    "";
            }


            if (resultProfit) {

                resultProfit.textContent =
                    "$0.00";
            }


            if (resultTotal) {

                resultTotal.textContent =
                    `$${amount.toFixed(2)}`;
            }


            if (resultFrequency) {

                resultFrequency.textContent =
                    `Maximum investment: $${maximumInvestment.toFixed(2)}`;
            }


            return;
        }


        

        clearError();


        

        let periodicProfit = 0;


        

        if (
            String(rateText)
                .toUpperCase()
                .includes("USD")
        ) {

            const baseInvestment =
                minimumInvestment > 0
                    ? minimumInvestment
                    : 1;


            periodicProfit =
                (amount / baseInvestment) *
                rate;
        }


        

        else {

            periodicProfit =
                amount *
                (rate / 100);
        }


        

        let totalProfit =
            periodicProfit;


        if (
            !isLifetime &&
            periods > 0
        ) {

            totalProfit =
                periodicProfit *
                periods;
        }


        

        const totalReturn =
            amount +
            totalProfit;


        

        if (profitInput) {

            profitInput.value =
                `$${periodicProfit.toFixed(2)}`;
        }


        

        if (resultInvestment) {

            resultInvestment.textContent =
                `$${amount.toFixed(2)}`;
        }


        

        if (resultRate) {

            resultRate.textContent =
                `${rate}%`;
        }


        

        if (resultProfit) {

            resultProfit.textContent =
                `$${periodicProfit.toFixed(2)}`;
        }


        

        if (resultTotal) {

            resultTotal.textContent =
                `$${totalReturn.toFixed(2)}`;
        }


        

        if (resultFrequency) {

            let cleanFrequency =
                String(frequency).trim();


            

            cleanFrequency =
                cleanFrequency.replace(
                    /^every\s+/i,
                    ""
                );


            if (isLifetime) {

                resultFrequency.textContent =
                    `$${periodicProfit.toFixed(2)} return every ${cleanFrequency} (Lifetime Plan)`;

            } else if (periods > 0) {

                resultFrequency.textContent =
                    `$${periodicProfit.toFixed(2)} return every ${cleanFrequency} for ${periodsText}`;

            } else {

                resultFrequency.textContent =
                    `$${periodicProfit.toFixed(2)} return every ${cleanFrequency}`;
            }
        }
    }


    

    planSelect.addEventListener(
        "change",
        calculateProfit
    );


    

    amountInput.addEventListener(
        "input",
        calculateProfit
    );


    

    resetCalculator();

});




document.addEventListener(
    "DOMContentLoaded",
    function () {

        const cards =
            document.querySelectorAll(
                ".testimonial-card"
            );

        const lines =
            document.querySelectorAll(
                ".page-line"
            );


        if (
            !cards.length ||
            !lines.length
        ) {
            return;
        }


        function showPage(page) {

            cards.forEach(
                function (card, index) {

                    const start =
                        (page - 1) * 2;

                    const end =
                        page * 2;


                    card.style.display =
                        (
                            index >= start &&
                            index < end
                        )
                            ? "block"
                            : "none";
                }
            );
        }


        lines.forEach(
            function (line) {

                line.addEventListener(
                    "click",
                    function () {

                        const page =
                            parseInt(
                                this.dataset.page
                            );


                        if (!isNaN(page)) {

                            showPage(page);
                        }
                    }
                );
            }
        );


        showPage(1);
    }
);




function initReadMoreButtons() {

    const modal =
        document.getElementById(
            "newsModal"
        );

    const modalBody =
        document.getElementById(
            "modal-body"
        );

    const closeBtn =
        document.querySelector(
            ".close-btn"
        );


    if (
        !modal ||
        !modalBody
    ) {
        return;
    }


    document.querySelectorAll(
        ".read-more-btn"
    ).forEach(
        function (btn) {

            btn.onclick =
                function (e) {

                    e.preventDefault();


                    const id =
                        this.getAttribute(
                            "data-id"
                        );


                    if (!id) {
                        return;
                    }


                    fetch(
                        `/news/${id}/`,
                        {
                            headers: {
                                "X-Requested-With":
                                    "XMLHttpRequest"
                            }
                        }
                    )
                        .then(
                            function (response) {

                                if (!response.ok) {

                                    throw new Error(
                                        "Unable to load news article."
                                    );
                                }

                                return response.text();
                            }
                        )
                        .then(
                            function (html) {

                                modalBody.innerHTML =
                                    html;

                                modal.style.display =
                                    "block";
                            }
                        )
                        .catch(
                            function (error) {

                                console.error(
                                    "News loading error:",
                                    error
                                );
                            }
                        );
                };
        }
    );


    if (closeBtn) {

        closeBtn.onclick =
            function () {

                modal.style.display =
                    "none";
            };
    }


    

    window.addEventListener(
        "click",
        function (e) {

            if (
                e.target === modal
            ) {

                modal.style.display =
                    "none";
            }
        }
    );
}




document.addEventListener(
    "DOMContentLoaded",
    initReadMoreButtons
);




document.addEventListener(
    "ajaxContentLoaded",
    initReadMoreButtons
);




document.addEventListener(
    "click",
    function (e) {

        const pageButton =
            e.target.closest(
                ".page-btn"
            );


        if (!pageButton) {
            return;
        }


        e.preventDefault();


        const url =
            pageButton.getAttribute(
                "href"
            );


        if (!url) {
            return;
        }


        const newsContent =
            document.querySelector(
                "#news-content"
            );


        if (!newsContent) {
            return;
        }


        fetch(
            url,
            {
                headers: {
                    "X-Requested-With":
                        "XMLHttpRequest"
                }
            }
        )
            .then(
                function (response) {

                    if (!response.ok) {

                        throw new Error(
                            "Unable to load news page."
                        );
                    }

                    return response.text();
                }
            )
            .then(
                function (html) {

                    newsContent.innerHTML =
                        html;


                    document.dispatchEvent(
                        new Event(
                            "ajaxContentLoaded"
                        )
                    );
                }
            )
            .catch(
                function (error) {

                    console.error(
                        "News pagination error:",
                        error
                    );
                }
            );
    }
);




document.addEventListener(
    "DOMContentLoaded",
    function () {

        const counters =
            document.querySelectorAll(
                ".count"
            );


        if (!counters.length) {
            return;
        }


        const speed = 200;


        counters.forEach(
            function (counter) {

                function updateCount() {

                    const target =
                        Number(
                            counter.getAttribute(
                                "data-target"
                            )
                        ) || 0;


                    const current =
                        Number(
                            counter.innerText
                        ) || 0;


                    const increment =
                        Math.ceil(
                            target / speed
                        );


                    if (
                        current < target
                    ) {

                        counter.innerText =
                            current + increment;

                        setTimeout(
                            updateCount,
                            20
                        );

                    } else {

                        counter.innerText =
                            target.toLocaleString();
                    }
                }


                updateCount();
            }
        );
    }
);

