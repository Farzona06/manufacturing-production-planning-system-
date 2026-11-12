document.addEventListener("DOMContentLoaded", () => {
  const overview = document.getElementById("overviewChart");
  if (overview && window.Chart) {
    new Chart(overview, {
      type: "bar",
      data: { labels: ["Dush", "Sesh", "Chor", "Pay", "Jum", "Shan"],
        datasets: [{ label: "Ishlab chiqarish (namuna)", data: [42, 55, 48, 67, 61, 74], borderRadius: 6, backgroundColor: "#5277ff" }] },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: "#eef1f6" } }, x: { grid: { display: false } } } }
    });
  }
  const forecast = document.getElementById("forecastChart");
  if (forecast && window.forecastData && window.Chart) {
    const d = window.forecastData;
    new Chart(forecast, {
      type: "line",
      data: { labels: [...d.months.map(m => "Oy " + m), "Oy 13"],
        datasets: [{ label: "Ishlab chiqarish", data: [...d.values, d.next], borderColor: "#315efb", backgroundColor: "#315efb22", fill: true, tension: .3 }] },
      options: { responsive: true, plugins: { legend: { display: true } }, scales: { y: { beginAtZero: false } } }
    });
  }
});
