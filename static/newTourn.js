$(document).ready(function($) {
    $('form').submit(function() {
        if ($('#p1').val() !== '' && $('#p2').val() !== '') {
            var p1 = $("#p1").val();
            var p2 = $("#p2").val();
            var newDouble = $('<li>' + p1 + "/" + p2 + '</li>');
            newDouble.on('click', function() {
                $(this).remove(); // Attach the event handler *before* adding the element
            });
            $('ol').append(newDouble); // To put the new task at the top of the list
            $("#p1").val("");
            $("#p2").val("");
            return false; // So the change persists
        }
    });
    $("ol").sortable(); // Because what good is a to-do list that you can't sort? :)
});