$(document).ready(function(){
    // delete plant modal function
    $("#delete-modal").on("show.bs.modal", function(event){
        //Get the button that triggered the modal
        var button = $(event.relatedTarget);

        // Extract value from the custom data-* attribute to link the plant_id 
        var url = button.data("url");
        $(this).find('#confirm-delete').attr('href', url);
    });
    
    // checkbox validation function
    $( '.checkbox-validation' ).on('submit', function(e) {
        // checks if any inputs for suitable_for are checked 
        if($('input[name="suitable_for"]:checked').length === 0) {
            // prevents the submiting of the form
            e.preventDefault();
            // adds an * to label so users know it is required
            $('.suitable-for').text("Suitable For *");
        }
    });
});

