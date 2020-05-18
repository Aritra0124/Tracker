$(document).ready(function () {
    $('#monitor_activities').click(function () {
        $('#activity_list').show();
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

                var ita = data.length / 4 + 1;
                var p = parseInt(ita);
                var k = 0;
                for (var i = 0; i < p; i++) {
                    $("#tbody").append("<tr>");
                    for (var j = k; j < k + 4; j++) {
                        if (data[j] == null) {
                            break;
                        }
                        var eachrow = "<td>" + "<p class='name'>" + data[j] + "</p>" + "</td>";
                        $("#tbody").append(eachrow);   // Append new elements
                        //j = k+3;
                    }
                    $("#tbody").append("</tr>");

                    k = k + 4;
                }


                /* $.each(data, function (index, item) {
                     var eachrow = "<tr>" + "<td>"
                         + "<p class='name'>" + item[index] + "</p>" +
                         + "<p class='name'>" + item[index] + "</p>" +
                         + "<p class='name'>" + item[index] + "</p>" +
                         "</td>" + "</tr>";
                     $('#tbody').append(eachrow);

                 });*/


            },
                error: function (error) {
                    alert("No data found")
                    console.log(error);
                }
            });
    });
});
