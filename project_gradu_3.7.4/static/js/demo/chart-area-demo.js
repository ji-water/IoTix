// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var chart_date=["1", "2", "3", "4", "5", "6", "7"];
var chart_data=[0,0,0,0,0,0,0];
var chart_data2=[0,0,0,0,0,0,0];

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: chart_date,
    datasets: [{
      label: "길이 변화량",
      lineTension: 0.3,
      backgroundColor: "rgba(34,142,208,0.4)",
      borderColor: "rgba(34,142,208,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(34,142,208,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(34,142,208,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: chart_data
    },
    {
      label: "식물 길이",
      lineTension: 0.3,
      backgroundColor: "rgba(250,112,75,0.4)",
      borderColor: "rgba(250,112,75,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(250,112,75,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(250,112,75,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: chart_data2
    }]
  },
  options: {
    responsive:true,
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        },
        stacked: true,
      }],
      yAxes: [{
        stacked:true,
        ticks: {
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      //display: false
      labels:{
        usePointStyle: true}
    }
    }
}
);

$("#toggle").click(function() {
	 chartInstance.data.datasets.forEach(function(ds) {
    ds.hidden = !ds.hidden;
  });
  chartInstance.update();
});


var ctx2 = document.getElementById("myBarChart");
var myBarChart = new Chart(ctx2, {
  type: 'bar',
  data: {
    labels: [1,2,1,2,1,2,1],
    datasets: [{
      label: "성장 속도",
      lineTension: 0.3,
      backgroundColor: "rgba(253,183,43,1)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [0,0,0,0,0,0,0]
    }]
  },
  options:{
  legend: {
      display: false
    }
  }
});
