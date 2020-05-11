function activity_show() {
    var select = $('option:selected').val();
    /* if select personal from select box then show my text box */
    if (select == "none") {
        $('#create_activity').hide();
        $('#monitor_activity').hide();
        $('#delete_activity').hide();
    }
    if (select == "create_activity") {
        $('#create_activity').show();
        $('#monitor_activity').hide();
        $('#delete_activity').hide();
    }
    if (select == "monitor_activity") {
        $('#create_activity').hide();
        $('#monitor_activity').show();
        $('#delete_activity').hide();
    }
    if (select == "delete_activity") {
        $('#create_activity').hide();
        $('#monitor_activity').hide();
        $('#delete_activity').show();
    }
}
