$(document).ready(function () {
    $('#tbody').on('click', 'p', function () {
        //var value = $(this).id();
        var currentRow = $(this).closest("tr");
        var activity_name = currentRow.find(".name").html();
        $("#ac_name").html("");
        $("#ac_type").html("");
        $("#ac_target").html("");
        $.ajax({
            url: '/activity_details',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                activity_name: activity_name
            }),
            type: 'POST',
            success: function (response) {
                res = response;
                data = res["activities_details"];
                console.log(data["activity_name"])
                $('#ac_name').append(data["activity_name"]);
                $('#ac_type').append(data["activity_type"]);
                $('#ac_target').append(data["target_type"]);

                $('#show_data').show();
            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});