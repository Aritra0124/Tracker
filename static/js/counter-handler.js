$(document).ready(function () {
    $('#count_down').click(function () {
        $('#count_down_display').show();
        $('#create_activity').hide();
        $('#monitor_activity').hide();
        $('#delete_activity').hide();

    });

});


$(document).ready(function () {
    $('#start_counter').click(function () {
        var time_count = parseInt($('#time_count').val()) * 60;
        setInterval(function () {
            time_count--;
            if (time_count >= 0) {
                $('#show_counter').html("")
                $('#show_counter').append(time_count);
                if (time_count == 0) {
                    const audio = new Audio("../static/audio/music.mp3");
                    audio.play();
                    alert("Time's up");

                }
            }
        }, 1000)
    });
});