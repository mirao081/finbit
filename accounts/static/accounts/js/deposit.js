document.addEventListener("DOMContentLoaded", function () {
  const chartCanvas = document.getElementById("planComparisonChart");
  if (chartCanvas) {
    const ctx = chartCanvas.getContext("2d");

    const planLabels = JSON.parse(chartCanvas.dataset.labels || "[]");
    const planReturns = JSON.parse(chartCanvas.dataset.returns || "[]");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: planLabels,
        datasets: [
          {
            label: "Total Return",
            data: planReturns,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
        },
      },
    });
  }
});
function loadMarketData() {
  fetch(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd"
  )
    .then((response) => response.json())
    .then((data) => {
      const widget = document.getElementById("crypto-widget");
      if (widget) {
        widget.innerHTML = `
          <p><strong>Bitcoin (BTC):</strong> $${data.bitcoin.usd}</p>
          <p><strong>Ethereum (ETH):</strong> $${data.ethereum.usd}</p>
          <p><strong>Tether (USDT ERC20):</strong> $${data.tether.usd}</p>
          <p><strong>Tether (USDT TRC20):</strong> $${data.tether.usd}</p>
        `;
      }
    })
    .catch((err) => console.error("Market data error:", err));
}
loadMarketData();
setInterval(loadMarketData, 60000); 
document.addEventListener("DOMContentLoaded", function () {
  const carousel = document.querySelector(".testimonial-carousel");
  if (carousel) {
    let index = 0;
    const quotes = carousel.querySelectorAll("blockquote");

    function showQuote(i) {
      quotes.forEach((q, idx) => {
        q.style.display = idx === i ? "block" : "none";
      });
    }

    showQuote(index);
    setInterval(() => {
      index = (index + 1) % quotes.length;
      showQuote(index);
    }, 5000);
  }
});
document.addEventListener("DOMContentLoaded", function () {
  const chatBtn = document.querySelector(".chat-btn");
  if (chatBtn) {
    chatBtn.addEventListener("click", () => {
      alert("Connecting you to support chat...");
    });
  }
});
