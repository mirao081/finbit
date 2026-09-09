document.addEventListener("DOMContentLoaded", function () {
"use strict";




const planSelect = document.getElementById("planSelect");
const investAmount = document.getElementById("investAmount");

const displayInvestment =
    document.getElementById("displayInvestment");

const profitAmount =
    document.getElementById("profitAmount");

const totalReturn =
    document.getElementById("totalReturn");

const calculatorRange =
    document.getElementById("calculatorRange");

const errorBox =
    document.getElementById("calcError");




if (
    !planSelect ||
    !investAmount ||
    !displayInvestment ||
    !profitAmount ||
    !totalReturn ||
    !calculatorRange ||
    !errorBox
) {
    return;
}




function formatMoney(value) {
    if (!Number.isFinite(value)) {
        value = 0;
    }

    return "$" + value.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}




function clearResults() {
    displayInvestment.textContent = "$0.00";
    profitAmount.textContent = "$0.00";
    totalReturn.textContent = "$0.00";

    errorBox.textContent = "";
    errorBox.classList.remove("error", "success");
}




function getSelectedPlan() {
    const option =
        planSelect.options[planSelect.selectedIndex];

    if (!option || !option.value) {
        return null;
    }

    const rate = parseFloat(option.dataset.rate);
    const min = parseFloat(option.dataset.min);

    let max = Infinity;

    if (
        option.dataset.max !== undefined &&
        option.dataset.max !== ""
    ) {
        max = parseFloat(option.dataset.max);
    }

    return {
        id: option.value,
        name: option.textContent.trim(),
        rate: Number.isFinite(rate) ? rate : 0,
        min: Number.isFinite(min) ? min : 0,
        max: Number.isFinite(max) ? max : Infinity
    };
}




function updatePlanRange(plan) {
    if (!plan) {
        calculatorRange.textContent =
            "Select a plan to see the investment range.";

        return;
    }

    if (Number.isFinite(plan.max)) {

        calculatorRange.textContent =
            "Investment range: " +
            formatMoney(plan.min) +
            " – " +
            formatMoney(plan.max);

    } else {

        calculatorRange.textContent =
            "Minimum investment: " +
            formatMoney(plan.min);

    }
}




function resetCalculator() {

    investAmount.value = "";
    investAmount.disabled = true;

    investAmount.removeAttribute("min");
    investAmount.removeAttribute("max");

    investAmount.placeholder =
        "Select a plan first";

    calculatorRange.textContent =
        "Select a plan to see the investment range.";

    clearResults();
}




function preparePlan(plan) {

    if (!plan) {
        resetCalculator();
        return;
    }

    investAmount.disabled = false;

    investAmount.placeholder =
        "Enter investment amount";

    investAmount.min = plan.min;

    if (Number.isFinite(plan.max)) {
        investAmount.max = plan.max;
    } else {
        investAmount.removeAttribute("max");
    }

    updatePlanRange(plan);
}




function calculateProfit() {

    const plan = getSelectedPlan();

    if (!plan) {
        resetCalculator();
        return;
    }

    preparePlan(plan);

    clearResults();

    const rawAmount =
        investAmount.value.trim();

    

    if (!rawAmount) {
        return;
    }


    

    const amount = parseFloat(rawAmount);


    

    if (
        !Number.isFinite(amount) ||
        amount <= 0
    ) {

        errorBox.textContent =
            "Please enter a valid investment amount.";

        errorBox.classList.add("error");

        return;
    }


    

    if (amount < plan.min) {

        displayInvestment.textContent =
            formatMoney(amount);

        errorBox.textContent =
            "Minimum investment for " +
            plan.name +
            " is " +
            formatMoney(plan.min) +
            ".";

        errorBox.classList.add("error");

        return;
    }


    

    if (
        Number.isFinite(plan.max) &&
        amount > plan.max
    ) {

        displayInvestment.textContent =
            formatMoney(amount);

        errorBox.textContent =
            "Maximum investment for " +
            plan.name +
            " is " +
            formatMoney(plan.max) +
            ".";

        errorBox.classList.add("error");

        return;
    }


    

    const profit =
        amount * (plan.rate / 100);

    const total =
        amount + profit;


    

    displayInvestment.textContent =
        formatMoney(amount);

    profitAmount.textContent =
        formatMoney(profit);

    totalReturn.textContent =
        formatMoney(total);


    

    errorBox.textContent =
        plan.rate +
        "% estimated return calculated.";

    errorBox.classList.add("success");
}




planSelect.addEventListener(
    "change",
    function () {

        

        investAmount.value = "";

        clearResults();

        const plan = getSelectedPlan();

        if (!plan) {
            resetCalculator();
            return;
        }

        preparePlan(plan);

        

        investAmount.focus();
    }
);




investAmount.addEventListener(
    "input",
    function () {
        calculateProfit();
    }
);




resetCalculator();


});
