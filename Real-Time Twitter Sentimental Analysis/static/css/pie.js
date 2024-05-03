function animateStart(a , b) {
    var ctx = document.getElementById('myChart').getContext("2d");
    new Chart(ctx, {
    type: 'pie',
    data: {
    labels: ['POSITIVE(%)', 'NEGATIVE(%)'],
    datasets: [{
    
    label: 'Reviews',
    
    data:[a,b],
    backgroundColor:[
    '#f2672e',
    '#0AA344'
    ],
    borderWidth: 0
    }]
    },
    options: {
    scales: {
    y: {
        beginAtZero: true
        }
    }
    }
    });
}