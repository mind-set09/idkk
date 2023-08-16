document.addEventListener("DOMContentLoaded", function () {
  updateLiveInfo();
});

function updateLiveInfo() {
  // Simulate retrieving live information
  const cpuUsage = "23.67%";
  const memoryUsage = "379.98 MB";
  const networkActivity = "3.7Mbps";
  const pythonVersion = "3.10.12";
  const platform = "Linux 5.10.0-24-amd64";

  // Update the live information on the dashboard
  document.getElementById("cpu-usage").textContent = cpuUsage;
  document.getElementById("memory-usage").textContent = memoryUsage;
  document.getElementById("network-activity").textContent = networkActivity;
  document.getElementById("python-version").textContent = pythonVersion;
  document.getElementById("platform").textContent = platform;
}
