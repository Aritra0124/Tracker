$(document).ready(function () {
    $('#add_activity').click(function () {
        var activity_name = $('#activity_name').val();
        var activity_type = $("#activity_type option:selected").val();
        var target_type = $("#target_type option:selected").val()
        var activity_note = $('#activity_note').val();
        console.log(activity_type, target_type)
        $.ajax({
            url: '/add_activity',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                activity_name: activity_name,
                activity_type: activity_type,
                target_type: target_type,
                activity_note: activity_note
            }),
            type: 'POST',
            success: function (response) {
                res = response;
                console.log(response);
                //if (res["status code"] == 200){
                alert(res["status"]);
                $("#activity_name").trigger("reset");
                //}
            },

            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
