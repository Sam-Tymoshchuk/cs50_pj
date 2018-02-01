$(function() {
    $("#q").bind("click", function() {

        let param = {
            login: "Sam",
            pass: "123"
        };
        $.getJSON("/login", param, function(data, textStatus, jqXHR) {

            $("#p").replaceWith(
                ""
                );
        });
        return false;
    });
});