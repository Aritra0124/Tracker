$(function () {
    $('button').click(function () {
        var username = $('#email').val();
        var password = $('#psw').val();
        $.ajax({
            url: '/login',
            dataType: "Json",
            data: {
                username: username,
                password: password
            },
            type: 'POST',
            success: function (response) {
                res = response;
                console.log("Working");
                console.log(response);
                alert(res["status"]);
                $('#show').show();

            },
            error: function (error) {
                alert("No data found")
                console.log(error);
            }
        });
    });
});
