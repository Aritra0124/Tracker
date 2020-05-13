$(document).ready(function () {
    $('#create_login').click(function () {
        var username = $('#create_username').val();
        var email_id = $('#create_email').val();
        var password = $('#create_psw').val();
        $.ajax({
            url: '/create_login',
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                username: username,
                email_id: email_id,
                password: password
            }),
            type: 'POST',
            success: function (response) {
                res = response;

                if (res["status"] == "Invalid") {
                    alert(res["status"]);
                } else {
                    alert(res["status"]);
                }
                $("#create_username").html("");
                $("#create_email").html("");
            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
