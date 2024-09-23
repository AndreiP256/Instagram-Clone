// script.js
window.onload = function() {
    // Get the data from the hidden elements
    var imagesPerCategory = JSON.parse(document.getElementById('imagesPerCategory').textContent);

    // Define colors for the pie slices
    var backgroundColors = ['rgba(255,0,184,1)', 'rgba(165,0,215,1)', 'rgba(75,0,245,1)', 'rgba(0,120,255,1)', 'rgba(100,255,255,1)'];
    var borderColors = backgroundColors.map(color => color.replace('1)', '0.8)'));
    // Create the chart
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: imagesPerCategory.map(item => item.category),
            datasets: [{
                data: imagesPerCategory.map(item => item.count),
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Images per Category'
                }
            },
        },
    });
}