$(function(){

    google.charts.load('current', {packages: ['corechart', 'line']});
    google.setOnLoadCallback(drawChart);

    const thresold = 0.5;

    // assume we only have 2 abnormalous events in video
    const starting_01 = annotation[0][0]; // first temporal annotation
    const ending_01 = annotation[0][1];

    starting_02 = -1; // second temporal annotation
    ending_02 = -1;
    if(annotation.length==2){
        starting_02 = annotation[1][0]; 
        ending_02 = annotation[1][1];
    }


    var annotationColor = '#ff00ff';

    function toPair(arr) {
        var rv = [];
        for (var i = 0; i < arr.length; ++i){
            if (starting_01==ending_01){ // FORs NORMAL video, no temporal annotation!
                rv.push([i+1, thresold, arr[i], 0, null,null]);
            }
            else{ // FOR ABNORMAL video
                if(i==starting_01 || i==starting_02){
                    rv.push([i+1, thresold, arr[i], 0, 'Starting frame ' + i.toString(), 'Starting abnormal interval. Frame ' + i.toString()]);
                }
                else if (i==ending_01 || i==ending_02){
                    rv.push([i+1, thresold, arr[i], 0,'Ending frame ' + i.toString(), 'Ending abnormal interval. Frame ' + i.toString()]);
                }
                else if(i>starting_01 && i < ending_01){
                    rv.push([i+1, thresold, arr[i], 1.0, null, null]);
                }
                else if(i>starting_02 && i < ending_02){
                    rv.push([i+1, thresold, arr[i], 1.0, null, null]);
                }
                else rv.push([i+1, thresold, arr[i], 0, null, null]);
            }
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
            },
        };
        function selectHanlder() {
            var selectedItem =  chart.getSelection()[0];
            if (selectedItem) {
                var frame = data.getValue(selectedItem.row, 0);
                $('#video-player')[0].currentTime = frame/video.frameRate;
            }
        }
        var chartDiv = document.getElementById('curve_chart');
        var chart = new google.visualization.LineChart(chartDiv);
        google.visualization.events.addListener(chart, 'select', selectHanlder);
        chart.draw(data, options);
    }

    const video = VideoFrame({
        id : 'video-player',
        frameRate: 29.97,
        callback : function(numberFrame) {
            if (numberFrame % 10 == 1){
                drawChart(numberFrame);
            }
            if(scores.length - numberFrame < 10){
                drawChart(scores.length);
            }
        }
    });

    $('#plot-score').click(function() {
        video.video.pause();
        let nFrame = scores.length;
        drawChart(nFrame);
        $("#play-pause").html('<img src="https://iconsplace.com/wp-content/uploads/_icons/ffffff/256/png/play-icon-18-256.png" style="height:23px;margin-bottom:2px"/> Play');
    });

    $('#play-pause').click(function(){
        video.frameRate = scores.length/ $('#video-player')[0].duration;
        ChangeButtonText();
    });

    function ChangeButtonText(){
        if(video.video.paused){
            video.video.play();
            video.listen('frame');   
            $("#play-pause").html('<img src="https://iconsplace.com/wp-content/uploads/_icons/ffffff/256/png/pause-icon-18-256.png" style="height:23px;margin-bottom:2px"/> Pause');
        }else{
            video.video.pause();
            video.stopListen();
            $("#play-pause").html('<img src="https://iconsplace.com/wp-content/uploads/_icons/ffffff/256/png/play-icon-18-256.png" style="height:23px;margin-bottom:2px"/> Play');
        }
    }
    // if(isC3Dnew) {
    //     $.ajax({
    //         type: 'POST',
    //         url: '/catalog/get-score',
    //         data: {
    //             no_segment: $(this).attr('data-segment'),
    //             isC3Dnew,
    //             video_path: video_path,
    //             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    //         },
    //         success: function (data){
    //             scores = data.scores;
    //             nFrame = scores.length;
    //             drawChart(nFrame);
    //         }
    //     })
    // }

    $('input[type=radio][name=weightName]').change(function () {
        $("#modal-progress").modal("show");
        let data = {
            no_segment: $(this).attr('data-segment'),
            weights_path: this.value,
            isC3Dnew,
            video_path: video_path,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        }
        if (isC3Dnew){
            data['id'] = video_id;
        }
        console.log(data)
        $.ajax({
            type: 'POST',
            url: '/catalog/get-score',
            data,
            success: function (data) {
                scores = data.scores;
                video.frameRate = scores.length/ $('#video-player')[0].duration;
                drawChart(scores.length);
            },
            complete: function () {
                $("#modal-progress").modal("hide");
            }
        })
    })
})