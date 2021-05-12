// const button = document.querySelector("#likePlant");
// button.addEventListener('click', function() {
//     button.classList.toggle("fas")
//     button.classList.toggle("far")
// })

$(document).ready(function(){
    $("#delete-modal").on("show.bs.modal", function(event){
        //Get the button that triggered the modal
        var button = $(event.relatedTarget);

        // Extract value from the custom data-* attribute
        var url = button.data("url");
        $(this).find('#confirm-delete').attr('href', url)
    });
});

