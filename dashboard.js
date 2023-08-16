document.addEventListener("DOMContentLoaded", function () {
  updateLiveInfo();
});

async function updateLiveInfo() {
  try {
    const response = await fetch("/get_live_info", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const liveInfo = await response.json();
      updateLiveInfoOnPage(liveInfo);
    } else {
      console.error("Failed to fetch live info");
    }
  } catch (error) {
    console.error("Error fetching live info:", error);
  }
}

function updateLiveInfoOnPage(liveInfo) {
  document.getElementById("cpu-usage").textContent = liveInfo.cpuUsage;
  document.getElementById("memory-usage").textContent = liveInfo.memoryUsage;
  document.getElementById("network-activity").textContent = liveInfo.networkActivity;
  document.getElementById("python-version").textContent = liveInfo.pythonVersion;
  document.getElementById("platform").textContent = liveInfo.platform;
}
