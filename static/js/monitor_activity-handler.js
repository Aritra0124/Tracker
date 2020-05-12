$(document).ready(function () {
    $('#operation').on("change", function () {
        if ($('#operation').val() == "monitor_activity") {
            $("#tbody").html("");
            $('#show_data').hide();

            $.ajax({
                url: '/activities',
                dataType: "json",
                contentType: "application/json",
                data: {},
                type: 'GET',
                success: function (response) {
                    res = response;
                    data = res["activities"]

                    $.each(data, function (index, item) {
                        var eachrow = "<tr>"
                            + "<td>" + "<p class='name'>" + item + "</p>" + "</td>"
                            + "</tr>";
                        $('#tbody').append(eachrow);

                    });


                },
                error: function (error) {
                    alert("No data found")
                    console.log(error);
                }
            });
        }
    });
});
