// Load the Visualization API and the piechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table, 
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

  // Memory chart
  var $memoryElement = document.getElementById('memory-chart');
  var size = parseInt($memoryElement.getAttribute('data-size'))/2**20;
  var used = parseInt($memoryElement.getAttribute('data-usage'))/2**20;
  console.log(size, used);
  var data = google.visualization.arrayToDataTable([
    ['Usation', 'Percentage'],
    ['Free', size-used],
    ['Used', used]
  ]);

  var options = {
    title: 'Memory usage'
  };
  var chart = new google.visualization.PieChart($memoryElement);
  chart.draw(data, options);
}
