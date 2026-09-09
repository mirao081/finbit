document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("profitGrowthChart").getContext("2d");
  const labels = JSON.parse(document.getElementById("profitLabels").textContent);
  const dataPoints = JSON.parse(document.getElementById("profitData").textContent);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Profit Growth (USD)",
        data: dataPoints,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        tooltip: { enabled: true }
      },
      scales: {
        x: { title: { display: true, text: "Date" } },
        y: { title: { display: true, text: "Profit (USD)" } }
      }
    }
  });
});
