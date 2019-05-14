
google.charts.load('current', {packages: ['corechart', 'line']});
// google.charts.setOnLoadCallback(drawChart);
const thresold = 0.5;
const starting_frm = annotation[0][0]
const ending_frm = annotation[0][1]

console.log(annotation)
var annotationColor = '#ff00ff';

function toPair(arr) {
    var rv = [];
    for (var i = 0; i < arr.length; ++i){
        if(i==starting_frm){
            rv.push([i+1, thresold, arr[i], 0, 'Starting frame ' + i.toString(), 'Starting abnormal interval. Frame ' + i.toString()]);
        }
        else if (i==ending_frm){
            rv.push([i+1, thresold, arr[i], 0,'Ending frame ' + i.toString(), 'Ending abnormal interval. Frame ' + i.toString()]);
        }
        else if(i>starting_frm && i < ending_frm){
            rv.push([i+1, thresold, arr[i], 1.0, null, null]);
        }
        else rv.push([i+1, thresold, arr[i], 0, null, null]);
    }
      
    return rv;
}


function drawChart(nFrame) {
    var tmp = []; // temporary array to hold the scores from 1 to current frame
    // starting frame = 1 --> draw header --> fix this
     if (nFrame == 1){
         // create dummy data
         tmp = [0.0];
     }
     else{
        tmp = scores.slice(1,nFrame);
     }
    var data = new google.visualization.DataTable();
    var arrData = toPair(tmp);
    arrData.unshift([
        {label: 'Frame number', type: 'string'},
        {label: 'Thresold', type: 'number'},
        {label: 'Score', type: 'number'},
        {label: 'Ground truth', type: 'number'},
        {type: 'string', role: 'annotation'},
        {type: 'string', role: 'annotationText'}]); // push header to the begining of array 
    var data = google.visualization.arrayToDataTable(arrData);
    console.log(data);
    var options = {
        title: 'Anormaly Score',
        curveType: 'function',
        // width: 500,
        // height: 400,,
        hAxis: {
            title: 'Frame number',
            viewWindowMode: 'explicit',
            viewWindow: {
                min:0,
                max:scores.length
            }
        },
        vAxis: {
            title: 'Score (0-1)',
            viewWindowMode: 'explicit',
            viewWindow: {
                min:0.0,
                max:1.0
            },
            ticks: [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        },
        annotations: {
            stem: {
                color: annotationColor
            },
            textStyle: {
                bold: true,
                italic: true,
                // The color of the text.
                color: '#494545',
                // The color of the text outline.
                opacity: 0.8
              },
            style: 'line',
                    
        },
        legend: { position: 'top' },
        series: {
            0: {
                // set options for the first data series
                lineWidth: 1,
                areaOpacity: 0.1,
                color: 'blue',
                type: 'area'
            },
            1: {
                // set options for the second data series
                lineWidth: 3,
                areaOpacity: 0.2,
                color: 'red',
                type: 'area'
            },
            2: {
                // set options for the third data series
                lineWidth: 2,
                areaOpacity: 0.3,
                color: '#00D717',
                type: 'area'
            }
        }
    };
    var chartDiv = document.getElementById('curve_chart');
    var chart = new google.visualization.LineChart(chartDiv);
    chart.draw(data, options);
    }

let numberFrame = 0;
let frameRate = 29.97;
const video = VideoFrame({
    id : 'video',
    frameRate,
    callback : function(numberFrame) {
        
        if (numberFrame % 25 == 1){
            drawChart(numberFrame);
        }
    }
});

$('#plot-score').click(function() {
    let nFrame = scores.length;
    drawChart(nFrame);
});


$('#play-pause').click(function(){
    ChangeButtonText();
});

function ChangeButtonText(){
  if(video.video.paused){
        video.video.play();
        video.listen('frame');
        $("#play-pause").html('Pause');
    }else{
        video.video.pause();
        video.stopListen();
        $("#play-pause").html('Play');
    }
  }
  function plotScore(numberOfFrame){
    var totalFrame = scores.length;

    var margin = {top: 50, right: 50, bottom: 50, left: 50}
        , width = 500 - margin.left - margin.right 
        , height = 300 - margin.top - margin.bottom;

    var xScale = d3.scaleLinear()
        .domain([0, totalFrame - 1])
        .range([0, width]);

    var yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);

    var line = d3.line()
        .x((d, i) => { return xScale(i); })
        .y((d) => { return yScale(d); })
        .curve(d3.curveMonotoneX);
    
    d3.select(".svg").html('');

    var svg = d3.select(".svg").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale));

    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale));
    
    svg.append("path")
        .datum(scores.slice(1, numberOfFrame))
        .attr("class", "line")
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", line);
}
