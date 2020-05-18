$(document).ready(function () {
    $('#activity_creation').click(function () {
        $('#count_down_display').hide();
        $('#create_activity').show();
        $('#monitor_activity').hide();
        $('#delete_activity').hide();

    });

});

$(document).ready(function () {
    $('#monitor_activities').click(function () {
        $('#count_down_display').hide();
        $('#create_activity').hide();
        $('#monitor_activity').show();
        $('#delete_activity').hide();

    });

});

$(document).ready(function () {
    $('#delete_activities').click(function () {
        $('#count_down_display').hide();
        $('#create_activity').hide();
        $('#monitor_activity').hide();
        $('#delete_activity').show();

    });

});
