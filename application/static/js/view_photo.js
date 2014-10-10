var data = [];
var settings = {
    align: {
        'y': 'bottom'
    },
    offset: {
        'top': 0//offset.top
    },

        'handlers': { click: function(event){

                        console.log(event.data)
                    },
                        mouseenter: 'show',
                        mouseleave: 'hide'
    }
};

$(document).ready(function(){

/*********** Document Globals *************************************************/
var $e = $("#image");
var offset = $("#image").offset();
$.fn.editable.defaults.mode = 'inline';

/************** Load Static Data *****************************************/
$.getJSON("/users", function(data){
  $.each(data.users, function(index, element){
     $("#new-tag-select").append($("<option></option>")
                        .attr("value",element.id)
                        .text(element.first_name+" "+element.last_name));
  });

});
function create_tags(){
    $.getJSON("/photos/"+thephotoid+"/tags", function(rsp){
            data = rsp.tags;
        //$('.taggd').each(function (i, e) {
            //var $e = $(e);
            //$e.taggd('clear');
            $e.taggd(settings);
            //getSetup();
            console.log(data);
            //$e.taggd('items', [])
            $e.taggd('items', data);
            $("#tags").html("");
            $.each(data, function(index, element){
                var name = element.text;
                console.log(name);
                var person = $("<li></li>");
                    person.addClass("people-tag");
                    //person.addClass("label");
                    //person.addClass("label-info");
                    person.addClass("list-group-item");
                    person.data("name", name);
                    person.text(element.text);
                    person.css("margin-left", "5px");
                    person.css("margin-right", "5px");
                var dicon = $("<span data-text=\""+element.text+"\" data-name=\""+element.id+"\"></span>");
                    dicon.addClass("glyphicon");
                    dicon.addClass("delete-icon");
                    dicon.addClass("glyphicon-remove");
                    dicon.css("font-size", "10px");
                    dicon.css("margin-left", "5px");
                    //dicon.data("name", element.text);
                person.append(dicon);
                //person.css("margin-top", "10px");
                //person.css("margin-bottom", "5px");
                $("#tags").append(person);
                //$("#tags").append($("<br/>"));
                //$("#tags").append($("<br/>"));

            });
            $(".people-tag").on("mouseenter", function(){
                //console.log($(this).text());
                $(".taggd-item-hover:contains('"+$(this).text()+"')").addClass("show")
            });
            $(".people-tag").on("mouseleave", function(){
                //console.log($(this).text());
                $(".taggd-item-hover:contains('"+$(this).text()+"')").removeClass("show")
            });
            $(".delete-icon").on("click", function(){
              var tagid = $(this).data("name");
              var name = $(this).data("text");
              $.ajax({
                      url: "/albums/"+thealbumid+"/photos/"+thephotoid+"/tags/"+tagid,
                      method: "DELETE"
              }).done(function(data){
                  //console.log(data);
                  //window.location.href = "/albums/{{photo.album_id}}/photos/{{photo.id}}/tags/html";
                  $(".taggd-item-hover:contains('"+name+"')").remove();//Class("show")
                  create_tags();
              });
            });
            //$e.taggd('show');
        //});
    });
}
create_tags();
/********************* Load Static Views ***********************************************/
//$("#event-modal-body").load("/albums/"+thealbumid+"/photos/"+thephotoid+"/event/html");
$("#comments").load("/photos/"+thephotoid+"/comments/html");

/********** Process comments **********/


/********************* Create Editable Inputs ******************************************/
$('#caption').editable({
    type: 'textarea',
    pk: thephotoid,
    url: '/edit_photo',
    title: 'Enter Caption',
    success: function(response, newValue) {
        if(response.status == 'error') return response.msg;
        //msg will be shown in editable form
    }
});

$("#caption").css("border-bottom-width", "0px");
$('#date').editable({
    type: 'text',
    pk: thephotoid,
    url: '/edit_photo',
    title: 'Enter Date',
    success: function(response, newValue) {
        if(response.status == 'error') return response.msg;
        //msg will be shown in editable form
    }
});

$('#year').editable({
    type: 'text',
    pk: thephotoid,
    url: '/edit_photo',
    title: 'Enter year',
    success: function(response, newValue) {
        if(response.status == 'error') return response.msg;
        //msg will be shown in editable form
    }
});

/********************* Click Handlers **************************************************/
$("#add-location").on("click", function(e){
    //e.preventDefault();
    console.log("asdf");
    $("#fullsize-modal").toggle();
});
$(".people-tag").on("mouseenter", function(){
    console.log("hovering");
});

$("#image").on("click", function(e){
    var offset = $(this).offset();
    var x = e.clientX - offset.left;
    var y = e.clientY - offset.top;
    var width = $(this).width();
    var height = $(this).height();
    $("#new-tag-select").data("x", x/width);
    $("#new-tag-select").data("y", y/height);
    $('#tags-modal').modal('toggle');
});
$("#new-comment-text").keypress(function(event){
       if (event.keyCode == 13) {
            var comment = $(this).val();
            var element = $(this);
            var temp = {comment: comment};
            $.ajax({
                    url: "/photos/"+thephotoid+"/comments",
                    method: "POST",
                    data: JSON.stringify(temp),
                    contentType: "application/json"

            }).done(function(data){
                
                $("#comments").load("/photos/"+thephotoid+"/comments/html");
                element.val("");
            });
        }
});
$("#tag-edit").on("click", function(){
    // When clicking the edit tag button, load the edit tags page
    window.location.href = "/albums/"+thealbumid+"/photos/"+thephotoid+"/tags/html"
});

$("#tag-toggle").on("click", function(){
    // Toggle the tag display
    if($(this).data("state") == "show"){
        $e.taggd('clear');
        $(this).data("state", "hide");
    } else {
        $e.taggd(settings);
        $e.taggd('items', data);
        $(this).data("state", "show");
    }
});

    $("#new-user-tag").hide();
    $("#new-user-button").on("click", function(){
        console.log($(this).data("state"));
        if($(this).data("state") == "select"){
            $(this).data("state", "create");
            $("#new-user-tag").show();
            $("#new-tag-select").hide();
        } else {
            $(this).data("state", "select");
            $("#new-user-tag").hide();
            $("#new-tag-select").show();
        }
    });

    $("#save").on("click", function(){
            var x = $("#new-tag-select").data("x");
            var y = $("#new-tag-select").data("y");
            $('#tags-modal').modal('toggle');

        if($("#new-user-button").data("state") == "select"){
            var user = $("#new-tag-select").val();
            var temp = {x:x, y:y, user:user, type: "select"};
          } else {
                  var first_name = $("#user-first-name").val();
                  var last_name = $("#user-last-name").val();
                  var temp = {x:x,
                              y:y,
                              first_name: first_name,
                              last_name: last_name,
                              type: "create"
                             };
           }
            
        $.ajax({
                    url: "/photos/"+thephotoid+"/tags",
                    method: "POST",
                    data: JSON.stringify(temp), 
                    contentType: "application/json"
                }).done(function(data){
                    //window.location.href = "/albums/{{photo.album_id}}/photos/{{photo.id}}/tags/html";
                    create_tags();
                });

    });



$("#clockwise").on("click", function(){
    $.get("/albums/"+thealbumid+"/photos/"+thephotoid+"/rotate?angle=90", function(data){
        if($("#image").data("size")=="medium"){
            $("#image").html("<img src=\"/albums/"+thealbumid+"/photos/"+thephotoid+"/medium\">");
        } else {
        $("#image").html("<img src=\"/albums/"+thealbumid+"/photos/"+thephotoid+"/file\">");
        }
    });
});

$("#counter").on("click", function(){
    $.get("/albums/"+thealbumid+"/photos/"+thephotoid+"/rotate?angle=-90", function(data){
        if($("#image").data("size")=="medium"){
            $("#image").html("<img src=\"/albums/"+thealbumid+"/photos/"+thephotoid+"/medium\">");
        } else {
        $("#image").html("<img src=\"/albums/"+thealbumid+"/photos/"+thephotoid+"/file\">");
        }
    });
});

$("#edit-caption").on("click", function(){
    if($(this).data("editing") == "true"){

        var temp = {caption: $("#caption".val())};
        $.ajax({
            url: "/albums/"+thealbumid+"/photos/"+thephotoid,
            method: "PUT",
            data: JSON.stringify(temp),
            contentType: "application/json",
        }).done(function(data){
            console.log(temp);
            console.log(data);
            $("#caption").html("");
            $(this).removeClass("glyphicon-pencil");
            $(this).addClass("glyphicon-ok");
            $(this).data("editing", "false");
        })
    } else {
        $(this).addClass("glyphicon-pencil");
        $(this).removeClass("glyphicon-ok");
        $(this).data("editing", "true");
        $("#caption").html("<span class=\"label label-info\" id=\"caption\">Caption: "+thecaption+"</span>");
    }
});

$("#save-new-comment").on("click", function(){
    var comment = $("#comment-text").val();
    var temp = {comment: comment};
    $.ajax({
            url: "/photos/"+thephotoid+"/comments",
            method: "POST",
            data: JSON.stringify(temp),
            contentType: "application/json"

    }).done(function(data){
        
        $("#comments").load("/photos/"+thephotoid+"/comments/html");
    });
});

$(".delete-comment").on("click", function(){
    console.log("Delete Comment");
    var commentid = $(this).data("comment");
    $.ajax({
        url: "/photos/"+photoid+"/comments/"+commentid,
        method: "DELETE",
        data: JSON.stringify({comment: commentid}),
        contentType: "application/json"
    }).done(function(){
        $("#comment-"+commentid).remove();
        //$("#comments").load("/photos/"+thephotoid+"/comments/html");
    });
});
/*********** Modals ****************************************************/

$("#toggle-size").on("click", function(){
    // toggle the full picture view modal
    $("#fullsize-modal").modal('toggle');
});

$("#add-comment").on("click", function(){
    $("#add-comment-modal").modal('toggle');
});

/**** End Document Ready *****/
});
