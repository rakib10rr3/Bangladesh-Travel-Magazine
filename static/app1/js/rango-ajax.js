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
$('button').on('click',function (event) {
    event.preventDefault();
    var element=$(this);
    $.ajax({
        url:'/app1/like',
        type:'GET',
        data:{obj_id:element.attr("data-id")},
        dataType: "json",
        success : function(response){
            element.html(' ' + response);
        }
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

