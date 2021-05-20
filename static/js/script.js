$(document).ready(function(){
    $("#delete-modal").on("show.bs.modal", function(event){
        //Get the button that triggered the modal
        var button = $(event.relatedTarget);

        // Extract value from the custom data-* attribute
        var url = button.data("url");
        $(this).find('#confirm-delete').attr('href', url)
    });
    $("#profile-delete-modal").on("show.bs.modal", function(event){
        //Get the button that triggered the modal
        var button = $(event.relatedTarget);

        // Extract value from the custom data-* attribute
        var url = button.data("url");
        $(this).find('#profile-confirm-delete').attr('href', url)
    });
    $( '.checkbox-validation' ).on('submit', function(e) {
        if($('input[name="suitable_for"]:checked').length === 0) {
            e.preventDefault();
            $('.suitable-for').text("Suitable For *");
        }
    });
});

