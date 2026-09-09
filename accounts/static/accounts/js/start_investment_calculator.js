document.addEventListener("DOMContentLoaded", function () {
    "use strict";


    

    const planSelect = document.getElementById("planSelect");
    const investAmount = document.getElementById("investAmount");

    const calculatorRange =
        document.getElementById("calculatorRange");

    const errorBox =
        document.getElementById("calcError");

    const profitAmount =
        document.getElementById("profitAmount");

    const resultFrequency =
        document.getElementById("resultFrequency");

    const resultInvestment =
        document.getElementById("resultInvestment");

    const resultRate =
        document.getElementById("resultRate");

    const resultProfit =
        document.getElementById("resultProfit");

    const resultTotal =
        document.getElementById("resultTotal");


    

    if (!planSelect || !investAmount) {
        return;
    }


    

    function formatMoney(value) {

        if (!Number.isFinite(value)) {
            value = 0;
        }

        return value.toLocaleString("en-US", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }


    

    function parseRate(value) {

        if (value === null || value === undefined) {
            return NaN;
        }

        const text = String(value).trim();

        if (!text) {
            return NaN;
        }

        

        const match = text.match(/-?\d+(?:\.\d+)?/);

        if (!match) {
            return NaN;
        }

        return Number(match[0]);
    }


    

    function cleanFrequency(value) {

        if (!value) {
            return "period";
        }

        let frequency = String(value)
            .trim()
            .replace(/\s+/g, " ");

        

        frequency = frequency
            .replace(/^every\s+/i, "Every ")
            .replace(/^each\s+/i, "Every ");


        return frequency;
    }


    

    function clearError() {

        if (!errorBox) {
            return;
        }

        errorBox.textContent = "";

        errorBox.classList.remove(
            "error",
            "success"
        );
    }


    function showError(message) {

        if (!errorBox) {
            return;
        }

        errorBox.textContent = message;

        errorBox.classList.remove("success");

        errorBox.classList.add("error");
    }


    

    function resetResults() {

        if (profitAmount) {
            profitAmount.textContent = "0.00";
        }

        if (resultInvestment) {
            resultInvestment.textContent = "$0.00";
        }

        if (resultRate) {
            resultRate.textContent = "0%";
        }

        if (resultProfit) {
            resultProfit.textContent = "$0.00";
        }

        if (resultTotal) {
            resultTotal.textContent = "$0.00";
        }

        if (resultFrequency) {
            resultFrequency.textContent =
                "Select a plan and enter an amount";
        }
    }


    

    function getSelectedPlan() {

        if (!planSelect.value) {
            return null;
        }

        const option =
            planSelect.options[
                planSelect.selectedIndex
            ];

        if (!option) {
            return null;
        }

        const rawRate =
            option.dataset.rate || "";

        const rate =
            parseRate(rawRate);


        const min =
            Number(option.dataset.min);


        const max =
            option.dataset.max &&
            option.dataset.max.trim() !== ""
                ? Number(option.dataset.max)
                : Infinity;


        const frequency =
            cleanFrequency(
                option.dataset.frequency
            );


        const duration =
            option.dataset.duration || "";


        const name =
            option.dataset.name || option.textContent.trim();


        return {
            id: option.value,
            name: name,
            rate: rate,
            min: min,
            max: max,
            frequency: frequency,
            duration: duration
        };
    }


    

    planSelect.addEventListener(
        "change",
        function () {

            clearError();

            const plan =
                getSelectedPlan();


            if (!plan) {

                investAmount.disabled = true;

                investAmount.value = "";

                resetResults();

                if (calculatorRange) {
                    calculatorRange.textContent =
                        "Select a plan to see its investment range.";
                }

                return;
            }


            

            investAmount.disabled = false;

            investAmount.value = "";


            

            if (Number.isFinite(plan.min)) {

                investAmount.min =
                    plan.min;

            } else {

                investAmount.removeAttribute("min");
            }


            

            if (Number.isFinite(plan.max)) {

                investAmount.max =
                    plan.max;

            } else {

                investAmount.removeAttribute("max");
            }


            

            if (calculatorRange) {

                if (Number.isFinite(plan.max)) {

                    calculatorRange.textContent =
                        `Investment range: $${formatMoney(plan.min)} – $${formatMoney(plan.max)}`;

                } else {

                    calculatorRange.textContent =
                        `Minimum investment: $${formatMoney(plan.min)} — No maximum limit`;
                }

            }


            

            resetResults();


            

            if (Number.isFinite(plan.rate)) {

                resultFrequency.textContent =
                    `${formatMoney(plan.rate)}% return ${plan.frequency.toLowerCase()}`;

            } else {

                resultFrequency.textContent =
                    `Return ${plan.frequency.toLowerCase()}`;
            }


            

            investAmount.focus();
        }
    );


    

    function calculateProfit() {

        clearError();


        const plan =
            getSelectedPlan();


        

        if (!plan) {

            resetResults();

            return;
        }


        

        if (!Number.isFinite(plan.rate)) {

            showError(
                "This investment plan has an invalid return rate."
            );

            resetResults();

            return;
        }


        

        const rawAmount =
            investAmount.value.trim();


        if (!rawAmount) {

            resetResults();

            resultFrequency.textContent =
                `${formatMoney(plan.rate)}% return ${plan.frequency.toLowerCase()}`;

            return;
        }


        const amount =
            Number(rawAmount);


        

        if (
            !Number.isFinite(amount) ||
            amount <= 0
        ) {

            showError(
                "Please enter a valid investment amount."
            );

            resetResults();

            return;
        }


        

        if (
            Number.isFinite(plan.min) &&
            amount < plan.min
        ) {

            showError(
                `Minimum investment for ${plan.name} is $${formatMoney(plan.min)}.`
            );

            resetResults();

            resultFrequency.textContent =
                `${formatMoney(plan.rate)}% return ${plan.frequency.toLowerCase()}`;

            return;
        }


        

        if (
            Number.isFinite(plan.max) &&
            amount > plan.max
        ) {

            showError(
                `Maximum investment for ${plan.name} is $${formatMoney(plan.max)}.`
            );

            resetResults();

            resultFrequency.textContent =
                `${formatMoney(plan.rate)}% return ${plan.frequency.toLowerCase()}`;

            return;
        }


        

        const profit =
            amount * (plan.rate / 100);


        const totalReturn =
            amount + profit;


        

        profitAmount.textContent =
            formatMoney(profit);


        resultInvestment.textContent =
            `$${formatMoney(amount)}`;


        resultRate.textContent =
            `${formatMoney(plan.rate)}%`;


        resultProfit.textContent =
            `$${formatMoney(profit)}`;


        resultTotal.textContent =
            `$${formatMoney(totalReturn)}`;


        resultFrequency.textContent =
            `${formatMoney(plan.rate)}% return ${plan.frequency.toLowerCase()}`;
    }


    

    investAmount.addEventListener(
        "input",
        calculateProfit
    );


    investAmount.addEventListener(
        "change",
        calculateProfit
    );


    investAmount.addEventListener(
        "blur",
        calculateProfit
    );


    

    investAmount.disabled = true;

    resetResults();

});