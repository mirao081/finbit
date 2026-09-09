document.addEventListener("DOMContentLoaded", function () {
  const refreshBtn = document.getElementById("refreshNewsBtn");
  const searchInput = document.getElementById("newsSearch");
  setInterval(() => {
    window.location.reload();
  }, 300000);
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      window.location.reload();
    });
  }
  if (searchInput) {
    searchInput.addEventListener("keyup", function () {
      const query = this.value.toLowerCase();
      const cards = document.querySelectorAll(".news-card");
      cards.forEach(card => {
        const title = card.querySelector("h3").textContent.toLowerCase();
        const description = card.querySelector("p").textContent.toLowerCase();
        card.style.display =
          title.includes(query) || description.includes(query) ? "block" : "none";
      });
    });
  }
});
