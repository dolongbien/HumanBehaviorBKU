
function plotScore(numberOfFrame){

    var margin = {top: 50, right: 50, bottom: 50, left: 50}
        , width = 500 - margin.left - margin.right 
        , height = 300 - margin.top - margin.bottom;

    var xScale = d3.scaleLinear()
        .domain([0, numberOfFrame - 1])
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
        .datum(scores)
        .attr("class", "line")
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", line);
}

let numberFrame = 0;
let frameRate = 29.97;
const video = VideoFrame({
    id : 'video',
    frameRate,
    callback : function(numberFrame) {
        if (numberFrame % 25 == 1){
            plotScore(numberFrame);
        }
    }
});

$('#plot-score').click(function() {
    let nFrame = scores.length;
    plotScore(nFrame);
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

