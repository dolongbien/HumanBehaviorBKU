
const dataset = scores.map( (score) => {
    console.log(score.id);
    return {'x': score.id, 'score': score}
})



function plot(numberOfFrame){

    var margin = {top: 50, right: 50, bottom: 50, left: 50}
        , width = window.innerWidth - margin.left - margin.right 
        , height = window.innerHeight - margin.top - margin.bottom;

    var xScale = d3.scaleLinear()
        .domain([0, numberOfFrame - 1])
        .range([0, width]);

    var yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);

    var line = d3.line()
        .x((d, i) => { return xScale(i); })
        .y((d) => { return yScale(d.score); })
        .curve(d3.curveMonotoneX);

    var svg = d3.select("svg")
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
        .datum(dataset)
        .attr("class", "line")
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", line);
}

$('button.plot').click(function() {
    let totalFrame = scores.length;
    print(totalFrame)
    plot(totalFrame);
});


let numberFrame = 0;
let frameRate = 29.97;
const video = VideoFrame({
    id : 'video',
    frameRate,
    callback : function(frame) {
        console.log(numberFrame);
        numberFrame = frame;
        if (numberFrame % 25 == 1){
            plot(numberFrame);
        }
    }
});

console.log(video)


// video.on('playing', (event) => {
//     $('button.plot').trigger('click');
//     setTimeout({}, frameRate);
//     if(!video.paused){
//         console.log('continue');
//         video.trigger('click');
//     }
//     else{
//         console.log('paused');
//     }
//     // console.log($('video').seekToNextFrame())
// })



$('video').on('durationchange', (event) => {
  console.log('Not sure why, but the duration of the video has changed.');
});

// $( "button.plot" ).html( "Next Step..." )