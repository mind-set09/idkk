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

// Fetch bot stats
fetch('/bot_stats')
  .then(response => response.json())
  .then(data => {
    document.getElementById('ping').textContent = data.ping;
    document.getElementById('cpu-usage').textContent = data.cpu_usage;
    document.getElementById('memory-usage').textContent = data.memory_usage;
    document.getElementById('os-info').textContent = data.os_info;
    document.getElementById('python-version').textContent = data.python_version;
  });
