$(document).ready(function($) {
    $('#add').click(function() {
        if ($('#p1').val() !== '' && $('#p2').val() !== '') {
            var p1 = $("#p1").val();
            var p2 = $("#p2").val();
            var newDouble = $('<li>')
                .text(p1 + "\n" + p2)
                .addClass("list-group-item");
            $("#p1").focus();

            $('<input>').attr({
                type: 'hidden',
                value: (p1+","+p2),
                name: 'pla'
            }).prependTo(newDouble);
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

    $('li').on('dblclick', function() {
                $(this).remove(); // Attach the event handler *before* adding the element
            });

    $("ol").sortable(); // can sort the list, got it from Jquery UI
});