// Fetch server count and total users
async function fetchServerInfo() {
  try {
    const response = await fetch('/server_info'); // Replace with the endpoint for fetching server info
    const data = await response.json();

    const serverCount = data.serverCount;
    const totalUsers = data.totalUsers;

    document.getElementById('server-count').textContent = serverCount;
    document.getElementById('total-users').textContent = totalUsers;
  } catch (error) {
    console.error(error);
  }
}

// Fetch bot statistics
async function fetchBotStats() {
  try {
    const response = await fetch('/bot_stats'); // Replace with the endpoint for fetching bot stats
    const data = await response.json();

    document.getElementById('ping').textContent = `${data.ping} ms`;
    document.getElementById('cpu-usage').textContent = `${data.cpuUsage}%`;
    document.getElementById('memory-usage').textContent = `${data.memoryUsage}%`;
    document.getElementById('os-info').textContent = data.osInfo;
    document.getElementById('python-version').textContent = data.pythonVersion;
  } catch (error) {
    console.error(error);
  }
}

// Refresh bot info when button is clicked
document.getElementById('refresh-btn').addEventListener('click', () => {
  fetchServerInfo();
  fetchBotStats();
});

// Initial fetch when the page loads
fetchServerInfo();
fetchBotStats();
