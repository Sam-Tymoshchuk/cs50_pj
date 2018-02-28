$("#auth").submit(function(event) {

    // Stop form from submitting normally
    event.preventDefault();

    let param = {
        login: $("#login").val(),
        pass: $("#inputPassword1").val()
    };

    let posting = $.post("/login", param);

    posting.done(function(data){

        function alarm(status){
            $("#inputPassword1").addClass("is-invalid");
            $("#p").append($("<div>")
            .addClass("invalid-feedback")
            .html(status));
        }

        if (data.status === "1"){
            alarm("Please enter username AND password");
        }
        else if (data.status === "2"){
            alarm("Invalid username or password");
        }

    });
});

$(document).ready(function($) {
    $('#add').click(function() {
        if ($('#p1').val() !== '' && $('#p2').val() !== '') {
            var p1 = $("#p1").val();
            var p2 = $("#p2").val();
            var newDouble = $('<li>')
                .text(p1 + " / " + p2)
                .addClass("list-group-item");
            newDouble.on('dblclick', function() {
                $(this).remove(); // Attach the event handler *before* adding the element
            });
            $('<input>').attr({
                type: 'hidden',
                value: (p1+p2),
                name: 'bar'
            }).append('li');
            $('ol').append(newDouble); // To put the new task at the bottom of the list
            $("#p1").val("");
            $("#p2").val("");
            return false;
            // So the change persists
        }
        else {
            return false;
        }
    });
    $("ol").sortable(); // can sort the list, got it from Jquery UI
});