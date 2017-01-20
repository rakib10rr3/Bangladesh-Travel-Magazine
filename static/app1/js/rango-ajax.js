/*
$('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like_catagory', {catagory_id: catid}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    });
});
*/


$(document).ready(function() {
     $('#likes').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
                $.get('/app1/like_catagory/', {page_id: catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

});


/*
    $('#like_count').ready( function() {

    $("#likes").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
});



   $('.likes-button').click(function(){
        var catid;
        catid = $(this).attr("data-catid");
                $.get('/app1/like_catagory/', {page_id: catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });






*/

