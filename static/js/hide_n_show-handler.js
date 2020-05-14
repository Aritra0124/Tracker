$(document).ready(function () {
    $('#login_here').click(function () {
        if ($('#login_details').is(":hidden")) {
            $('#login_details').show();
            $('#user_details').hide();
        } else {
            $('#login_details').hide();
        }
    });
});

$(document).ready(function () {
    $('#create_account').click(function () {
        if ($('#user_details').is(":hidden")) {
            $('#user_details').show();
            $('#login_details').hide()
        } else {
            $('#user_details').hide();
        }
    });
});