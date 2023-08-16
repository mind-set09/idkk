// Function to update the terminal with error messages
function updateTerminal(message) {
  const terminalOutput = document.getElementById('terminal-output');
  terminalOutput.textContent += message + '\n';
  terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

// Function to update the bot information in the dashboard
function updateBotInfo(botInfo) {
  const pingElement = document.getElementById('ping');
  const cpuUsageElement = document.getElementById('cpu-usage');
  const memoryUsageElement = document.getElementById('memory-usage');
  const osInfoElement = document.getElementById('os-info');
  const pythonVersionElement = document.getElementById('python-version');
  
  pingElement.textContent = botInfo.ping + ' ms';
  cpuUsageElement.textContent = botInfo.cpu_usage + '%';
  memoryUsageElement.textContent = botInfo.memory_usage + '%';
  osInfoElement.textContent = botInfo.os_info;
  pythonVersionElement.textContent = botInfo.python_version;
}

// Dummy data for testing
const dummyBotInfo = {
  ping: '25',
  cpu_usage: '10',
  memory_usage: '70',
  os_info: 'Linux 5.4.0-1059-azure',
  python_version: '3.8.10'
};

// Update the bot information on page load
window.addEventListener('DOMContentLoaded', () => {
  updateBotInfo(dummyBotInfo);
});

// Example: Update bot information when a button is clicked
document.getElementById('refresh-btn').addEventListener('click', async () => {
  try {
    // Fetch bot information from the server
    // Replace this with your actual API endpoint
    const response = await fetch('/api/botinfo');
    const data = await response.json();
    
    // Update the bot information on the page
    updateBotInfo(data);
  } catch (error) {
    // Handle any errors and display in the terminal
    updateTerminal('Error: ' + error.message);
  }
});
