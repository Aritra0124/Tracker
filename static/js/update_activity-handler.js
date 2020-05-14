$(document).ready(function () {
    $('#add_update').click(function () {
        var activity_name = $("#ac_name").text();
        var to_time = $('#to_time').val();
        var from_time = $('#from_time').val();
        $.ajax({
            url: '/update_activity',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                activity_name: activity_name,
                to_time: to_time,
                from_time: from_time
            }),
            type: 'POST',
            success: function (response) {
                res = response;
                alert(res["status"]);


            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
