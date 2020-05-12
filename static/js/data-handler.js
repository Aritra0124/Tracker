$(document).ready(function () {
    $('#login').click(function () {
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
                $('#email').val("");
                $('#psw').val("");
                if (res["status"] == "Invalid") {
                    alert(res["status"]);
                } else {
                    alert(res["status"]);
                    $('#show').show();
                    $('#logout').show();
                    $('#myForm').hide();
                }

            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
