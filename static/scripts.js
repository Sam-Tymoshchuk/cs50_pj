$(document).ready(function() {
    $("#q").click(function() {

        let param = {
            login: $("#login").val(),
            pass: $("#inputPassword1").val()
        };
        $.getJSON("/verification", param, function(data, textStatus, jqXHR) {
            if (data.status === "1"){

                $("#inputPassword1").addClass("is-invalid");
                $("#p").append($("<div>")
                .addClass("invalid-feedback")
                .html("Invalid login or password"))
            }

        });
    });
});