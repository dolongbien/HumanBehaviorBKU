$(document).ready(function () {
    $.fn.onAvailable = function (fn) {
        var sel = this.selector;
        var timer;
        var self = this;
        if (this.length > 0) {
            fn.call(this);
        } else {
            timer = setInterval(function () {
                if ($(sel).length > 0) {
                    fn.call($(sel));
                    clearInterval(timer);
                }
            }, 50);
        }
    };
    $("#UCFHBHeader").onAvailable(function () {
        $(this).addClass("hide-for-small");
    });
});