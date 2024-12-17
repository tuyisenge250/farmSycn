const systemData = JSON.parse('{{ system_info|safe }}');
  const temperatureData = systemData.map(data => data.temperature_change);
  console.log(temperatureData);
  const timeData = systemData.map(data => data.last_update);
  console.log(timeData)
  const ctx = document.getElementById('lineChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: timeData, // X-axis: Timestamps
      datasets: [{
        label: 'Temperature (°C)',
        data: temperatureData, // Y-axis: Temperature values
        borderColor: '#466E50',
        backgroundColor: 'rgba(70, 110, 80, 0.2)',
        borderWidth: 2,
        tension: 0.4,
        fill: true,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Time',
            font: { size: 14 },
          }
        },
        y: {
          title: {
            display: true,
            text: 'Temperature (°C)',
            font: { size: 14 },
          },
          beginAtZero: false,
        }
      },
    }
  });