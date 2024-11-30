const ctx = document.getElementById('lineChart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['10am', '11am', '12am', '01am', '02am', '03am'],
    datasets: [{
      label: 'Sales',
      data: [60, 80, 40, 70, 50, 90],
      borderColor: '#e91e63',
      backgroundColor: 'rgba(233, 30, 99, 0.3)',
      fill: true,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      }
    }
  }
});
