$(document).ready(function () {
    $('#start_counter').click(function () {
        var time_count = parseFloat($('#time_count').val()) * 60;
        setInterval(function () {
            time_count--;
            if (time_count >= 0) {
                $('#show_counter').html("")
                $('#show_counter').append(time_count);
                if (time_count == 0) {
                    alert("Time's up");
                    $('#music').play();
                }
            }
        }, 1000)
    });
});