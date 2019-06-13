$(function () {
  function updateAfterUpload(data) {
    console.log(data);
    if (data.is_valid) {
      $("#gallery tbody").prepend(
        `<tr>
            <td>
              <a class='btn disabled' href='/catalog/c3d-new/${data.title}' style="padding: 0"> ${data.title} </a>
            </td>
            <td>
              <span> ${data.filesize}</span>
            </td>
            <td style="max-width: 147px">
            <div class='progress-wrapper progress-js'>
              <div class='progress-bar progress-base-js' role="progressbar" data-task-url="/celery-progress/${data.task_id}" data-task-id='${data.task_id}' aria-valuemin="0" aria-valuemax="100" style="background-color: #68a9ef; width: 0%;">&nbsp;</div>
            </div>
            </td>
            <td>
              <button type="submit" class="btn btn-danger js-delete-videos pull-right" data-type='DELETE' data-id='${data.id}'>
                <span class="glyphicon glyphicon-trash"></span> Xóa
              </button>
            </td>
          </tr>`
      )

      var progressUrl = `/celery-progress/${data.task_id}`;
      var celeryProgressBar = new CeleryProgressBar;
      // Get added tr and init progress bar
      var progressBarJs = $('.progress-base-js')[0];
      console.log(progressBarJs)
      celeryProgressBar.initProgressBar(progressUrl, {progressBarElement: progressBarJs});

    }
  }

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
      $(".progress-bar").css({ "width": strProgress });
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      updateAfterUpload(data.result);
    },

  });

  $('.js-url-modal').click(function () {
    $('#model-urls').modal('show');
  });
  
  function isURL(str) {
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
    return pattern.test(str);
  }

  $('.js-url-upload').click(async function (e) {
    var url = $('.input-url').val();
    var filename = $('.input-filename').val();

    // Validation form 
    if (!isURL(url)){
      $('.with-errors').css({'display':'block'});
      $('.input-url').css({'border-color': 'red'});
    }
    else {
      $('.with-errors').css({'display':'none'});
      $('.input-url').css({'border-color': '#ccc'});
    }
    $('.processing').css({'display': 'inline-block'});
    $.ajax({
      type: 'POST',
      url: '/catalog/video-upload',
      data: {
        url,
        filename,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function (data) {
        $('#model-urls').modal('hide');
        updateAfterUpload(data);
      },
      complete: function() {
        $('.processing').css({'display': 'none'});
      }
    });
    // var xhr = new XMLHttpRequest();
    // xhr.open('GET', 'https://cors-anywhere.herokuapp.com/'+ url, true);
    // xhr.responseType = 'blob';
    // xhr.onload = function()
    // {
    //   blob = xhr.response;
    //   var filename = $('.input-filename').val();
    //   if (filename === ''){
    //     filename = url.split('/').pop();
    //   }
    //   blob.name = filename;
    //   files = [blob];
    //   console.log(filename);
    //   console.log(files);
    //   $('#model-urls').modal('hide');
    //   $("#fileupload").fileupload('add', {files});
    // }
    // xhr.send();
  });

  $('.js-extract-feature').click(function () {
    var progress;
    $("#modal-progress").modal("show");
    for (progress = 0; progress <= 100; progress += 10) {
      var strProgress = progress + '%';
      console.log(strProgress);
      $(".progress-bar").css({ "width": strProgress });
      $(".progress-bar").text(strProgress);
    }
    $("#modal-progress").modal("hide");
  });

  $(document).on('click','.js-delete-videos' ,function () {
    console.log($(this).attr('data-type'));
    let closest_tr = $(this).closest('tr');
    $.ajax({
      type: 'POST',
      url: '/catalog/delete-videos',
      data: {
        type: $(this).attr('data-type'),
        // files: Array($(this).attr('data-url')),
        ids: Array($(this).attr('data-id')),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function (data) {
        if (data.success) {
          closest_tr.remove();
        }
        else
          console.log('delete error');
      }
    })
  });

  // Delete all videos
  $('.js-delete-all-video').click(function () {
    $.ajax({
      type: 'POST',
      url: '/catalog/delete-videos',
      data: {
        type: $(this).attr('data-type'),
        delete_all: true,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function (data) {
        if (data.success) {
          $('#gallery > tbody').empty();
        }
        else
          console.log('delete error');
      }
    })
  });

  $('.progress-bar-js').ready(function () {
    var listProcess = $('.progress-bar-js');
    var pattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    Array.from(listProcess).forEach(function(element) {
      var progressUrl = $(element).attr('data-task-url');
      var task_id = $(element).attr('data-task-id');
      if (pattern.test(task_id)){
        var celeryProgressBar = new CeleryProgressBar;
        celeryProgressBar.initProgressBar(progressUrl, {progressBarElement: element, progressBarMessageElement: $(element).closest('.progress-bar-message')});
      }
    })
  });
});