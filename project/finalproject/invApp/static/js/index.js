const totalViewChart = document.getElementById('total-views-chart');
const revenueChart = document.getElementById('revenue-chart');

new Chart(totalViewChart, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      label: 'Monthly sales in Thousands (k)',
      data: [30, 29, 39, 41, 45, 50, 45, 38, 30, 45, 56, 50],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return value + 'k'; // Append 'k' to the tick values
          }
        }
      }
    }
  }
});


new Chart(revenueChart, {
  type: 'line',
  data: {
    labels: ['Dec 6', 'Dec 7', 'Dec 8', 'Dec 9', 'Dec 10'],
    datasets: [{
      label: 'Total Revenue',
      data: [2000, 3000, 1000, 2000, 5000, 3000],
      borderWidth: 1
    },
  {
      label: 'Costs',
      data: [500, 800, 200, 500, 1500, 800],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
        }
      }
    }
  }
);

const data = {
  datasets: [
    {
      type: 'bar', // First dataset as a bar chart
      label: 'Sales',
      data: [30000, 29000, 39000, 41000, 45000, 50000, 45000, 38000, 30000, 45000, 56000, 50000],
      yAxisID: 'y',
    },
    {
      type: 'bar', // Second dataset also a bar chart
      label: 'Inventory',
      data: [15000, 13500, 17000, 20000, 21000, 23000, 20000, 17000, 13000, 20000, 25000, 23000],
      yAxisID: 'y',
    },
    {
      type: 'line', // Third dataset as a line chart
      label: 'Inventory Turnover',
      data: [12, 4, 11, 5, 11, 8, 5, 4, 5, 6, 10, 6],
      yAxisID: 'y2',
    }
  ],
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
};

const config = {
  data: data,
  options: {
    responsive: true,
    maintainAspectRatio: false, // Allow height customization
    scales: {
      y: {
        beginAtZero: true,
        type: 'linear',
        position: 'left',
      },
      y2: {
        beginAtZero: true,
        type: 'linear',
        position: 'right',
      }
    }
  }
};

new Chart(document.getElementById('mixed-chart'), config);



