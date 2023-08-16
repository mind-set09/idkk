// Fetch server info from the Flask app
fetch('/server_info')
  .then(response => response.json())
  .then(data => {
    document.getElementById('server-count').textContent = data.serverCount;
    document.getElementById('total-users').textContent = data.totalUsers;
  })
  .catch(error => {
    console.error('Error fetching server info:', error);
  });

// Fetch bot stats from the Flask app
fetch('/bot_stats')
  .then(response => response.json())
  .then(data => {
    document.getElementById('ping').textContent = `${data.ping} ms`;
    document.getElementById('cpu-usage').textContent = `${data.cpuUsage}%`;
    document.getElementById('memory-usage').textContent = `${data.memoryUsage}%`;
    document.getElementById('os-info').textContent = data.osInfo;
    document.getElementById('python-version').textContent = data.pythonVersion;
  })
  .catch(error => {
    console.error('Error fetching bot stats:', error);
  });
