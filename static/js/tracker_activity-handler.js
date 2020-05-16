function renderChart(data, labels, activity_name, daily_target) {
    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: activity_name,
                data: data,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [

                    'rgba(75, 192, 192, 1)'

                ],
                borderWidth: 5
            },
                {
                    label: 'Daily Target',
                    data: daily_target,
                    borderColor: 'rgb(194,67,67)',
                    borderWidth: 5
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}


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
                $('#ac_name').append(data["activity_name"]);
                $('#ac_type').append(data["activity_type"]);
                $('#ac_target').append(data["target_type"]);

                $('#show_data').show();

                renderChart(res["dataset"]["data"], res["dataset"]["labels"], data["activity_name"], res["dataset"]["target_time"]);
            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
