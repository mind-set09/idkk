document.addEventListener("DOMContentLoaded", function () {
  updateLiveInfo();
});

async function updateLiveInfo() {
  try {
    const webhookUrl = 'YOUR_WEBHOOK_URL'; // Replace with your actual webhook URL

    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        cpuUsage: '20%',
        memoryUsage: '300 MB',
        networkActivity: '1.5 Mbps',
        pythonVersion: '3.9.7',
        platform: 'Linux',
      }),
    });

    if (response.ok) {
      console.log('Webhook data sent successfully');
    } else {
      console.error('Failed to send webhook data');
    }
  } catch (error) {
    console.error('Error sending webhook data:', error);
  }
}
