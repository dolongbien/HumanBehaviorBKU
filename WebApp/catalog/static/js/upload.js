$(function () {

  $(".js-upload-videos").click(function () {
    $("#fileupload").click();
  });


  $("#fileupload").fileupload({
      dataType: 'json',
      sequentialUploads: true,
  
      start: function (e) {
        $("#modal-progress").modal("show");
      },
  
      stop: function (e) {
        $("#modal-progress").modal("hide");
      },
  
      progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },
  
      done: function (e, data) {
        if (data.result.is_valid) {
          $("#gallery tbody").prepend(
            "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
          )
        }
      }
  
    });

});

$(function() {
  $('.js-extract-feature').click(function() {
    var progress;
    $("#modal-progress").modal("show");
    for(progress = 0; progress <= 100; progress += 10){
      var strProgress = progress + '%';
      console.log(strProgress);
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    }
    $("#modal-progress").modal("hide");
  })
})