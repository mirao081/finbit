document.addEventListener("DOMContentLoaded", async function () {
  async function fetchMarketData() {
    const res = await fetch("https://api.coingecko.com/api/v3/global");
    const data = await res.json();

    const marketCapEl = document.getElementById("marketCap");
    const volumeEl = document.getElementById("volume24h");
    const btcDomEl = document.getElementById("btcDominance");

    if (marketCapEl) {
      marketCapEl.textContent = "Market Cap: $" + data.data.total_market_cap.usd.toLocaleString();
    }
    if (volumeEl) {
      volumeEl.textContent = "24h Volume: $" + data.data.total_volume.usd.toLocaleString();
    }
    if (btcDomEl) {
      btcDomEl.textContent = "BTC Dominance: " + data.data.market_cap_percentage.btc.toFixed(2) + "%";
    }
  }
  async function fetchCoinPrices() {
    const res = await fetch(
      "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd&include_24hr_change=true"
    );
    const data = await res.json();

    const btcPriceEl = document.getElementById("btcPrice");
    const btcChangeEl = document.getElementById("btcChange");
    if (btcPriceEl && btcChangeEl) {
      btcPriceEl.textContent = "$" + data.bitcoin.usd;
      btcChangeEl.textContent =
        (data.bitcoin.usd_24h_change > 0 ? "+" : "") + data.bitcoin.usd_24h_change.toFixed(2) + "%";
      btcChangeEl.className =
        "change " + (data.bitcoin.usd_24h_change >= 0 ? "positive" : "negative");
    }

    const ethPriceEl = document.getElementById("ethPrice");
    const ethChangeEl = document.getElementById("ethChange");
    if (ethPriceEl && ethChangeEl) {
      ethPriceEl.textContent = "$" + data.ethereum.usd;
      ethChangeEl.textContent =
        (data.ethereum.usd_24h_change > 0 ? "+" : "") + data.ethereum.usd_24h_change.toFixed(2) + "%";
      ethChangeEl.className =
        "change " + (data.ethereum.usd_24h_change >= 0 ? "positive" : "negative");
    }

    const usdtPriceEl = document.getElementById("usdtPrice");
    const usdtChangeEl = document.getElementById("usdtChange");
    if (usdtPriceEl && usdtChangeEl) {
      usdtPriceEl.textContent = "$" + data.tether.usd;
      usdtChangeEl.textContent =
        (data.tether.usd_24h_change > 0 ? "+" : "") + data.tether.usd_24h_change.toFixed(2) + "%";
      usdtChangeEl.className =
        "change " + (data.tether.usd_24h_change >= 0 ? "positive" : "negative");
    }
  }
  async function fetchTrendingCoins() {
    const res = await fetch("https://api.coingecko.com/api/v3/search/trending");
    const data = await res.json();
    const trendingEl = document.getElementById("trendingCoins");
    if (trendingEl) {
      trendingEl.textContent = data.coins.map(c => c.item.name).join(" • ");
    }
  }
  async function fetchTopGainersLosers() {
    const res = await fetch(
      "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"
    );
    const data = await res.json();
    const tbody = document.querySelector("#gainersLosersTable tbody");
    if (tbody) {
      tbody.innerHTML = "";
      data.forEach(coin => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${coin.name}</td>
          <td>$${coin.current_price}</td>
          <td class="${coin.price_change_percentage_24h >= 0 ? "positive" : "negative"}">
            ${coin.price_change_percentage_24h.toFixed(2)}%
          </td>`;
        tbody.appendChild(row);
      });
    }
  }
  async function fetchNews() {
    try {
      const res = await fetch("https://api.coingecko.com/api/v3/status_updates");
      const data = await res.json();
      const newsDiv = document.getElementById("cryptoNews");
      if (newsDiv) {
        newsDiv.innerHTML = "";
        data.status_updates.slice(0, 5).forEach(update => {
          const item = document.createElement("p");
          item.textContent = update.description;
          newsDiv.appendChild(item);
        });
      }
    } catch (err) {
      const newsDiv = document.getElementById("cryptoNews");
      if (newsDiv) {
        newsDiv.textContent = "No news available.";
      }
    }
  }
  async function renderChart() {
    const res = await fetch(
      "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
    );
    const data = await res.json();
    const prices = data.prices.map(p => p[1]);
    const labels = data.prices.map(p => new Date(p[0]).toLocaleDateString());

    const canvas = document.getElementById("btcUsdtChart");
    if (canvas) {
      const ctx = canvas.getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: "BTC/USDT",
            data: prices,
            borderColor: "#4CAF50",
            fill: false
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: false }
          }
        }
      });
    }
  }
  fetchMarketData();
  fetchCoinPrices();
  fetchTrendingCoins();
  fetchTopGainersLosers();
  fetchNews();
  renderChart();
  setInterval(() => {
    fetchMarketData();
    fetchCoinPrices();
    fetchTrendingCoins();
    fetchTopGainersLosers();
    fetchNews();
    renderChart();
  }, 60000);
});
