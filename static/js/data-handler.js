$(function () {
    $('button').click(function () {
        var username = $('#email').val();
        var password = $('#psw').val();
        $.ajax({
            url: '/login',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                username: username,
                password: password
            }),
            type: 'POST',
            success: function (response) {
                res = response;
                console.log("Working");
                console.log(response);
                $('#email').val("");
                $('#psw').val("");
                if (res["status"] == "Invalid") {
                    alert(res["status"]);
                } else {
                    alert(res["status"]);
                    $('#show').show();
                    $('#logout').show();
                }

            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
