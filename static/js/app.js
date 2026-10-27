// ---------- Grab the page elements we need ----------
const landingPage = document.getElementById("landing-page");
const dashboardPage = document.getElementById("dashboard-page");
const startBtn = document.getElementById("start-btn");
const backBtn = document.getElementById("back-btn");
const backendStatus = document.getElementById("backend-status");

// ---------- Switch between landing page and dashboard ----------
function showDashboard() {
  landingPage.classList.add("hidden");
  dashboardPage.classList.remove("hidden");
  window.scrollTo(0, 0);
}

function showLanding() {
  dashboardPage.classList.add("hidden");
  landingPage.classList.remove("hidden");
  window.scrollTo(0, 0);
}

startBtn.addEventListener("click", showDashboard);
backBtn.addEventListener("click", showLanding);

// ---------- Check that the FastAPI backend is reachable ----------
async function checkBackend() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    backendStatus.textContent = data.status === "ok"
      ? "Backend connected ✓"
      : "Backend returned an unexpected response";
  } catch (error) {
    backendStatus.textContent = "Backend not reachable. Is the server running?";
  }
}

checkBackend();