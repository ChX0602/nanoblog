var req;
var $j = jQuery.noConflict();
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendRequest() {
	if(window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	}
	else {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	console.log("sendRequest");
	req.onreadystatechange = handleResponse;
	req.open("GET", "/grumblr/get-grumbles", true);
	req.send();
}

function handleResponse() {
	if (req.readyState != 4 || req.status != 200) {
		return;
	}

	var grumbles = JSON.parse(req.responseText);
	var list = document.getElementById("post-list");
	for (var i = 0; i < grumbles.length; ++i) {
		var id = grumbles[i]["pk"];
		var date = grumbles[i]["fields"]["date"];
		var grumbleText = grumbles[i]["fields"]["text"];
		var dislikers = grumbles[i]["fields"]["dislikers"];
		var user = grumbles[i]["fields"]["user"];
        var user_name = grumbles[i]["fields"]["user_name"];
		var picture = grumbles[i]["fields"]["picture"];
        var newGrumble = document.createElement("li");
        newGrumble.setAttribute("class", "list-group-item");
        var profile_pic = "/grumblr/photo/"+id+"&"+user;
        var pic_url = "/grumblr/post-photo/"+id;
        var user_url = "/grumblr/follower-profile/"+user;
        var pic_block;
        if (picture!="")
        {
            pic_block = '<div class="row"><div class="col-xs-6 col-md-3"><a href='+pic_url+' class="thumbnail" style="width: 200px; height: 200p"><img src='+pic_url+' alt="..."></a></div></div>';
        }
        else
        {
            pic_block = "";
        }
		newGrumble.innerHTML = 
		'<div class="panel panel-default"><div class="panel-body"><div class="media"><a href = '+user_url+'><h6 id="poster-id">'+user_name+'</h6></a><p>'+date+'</p><a class="pull-left" href='+user_url+'><img class="media-object" src='+ profile_pic +' alt="..." height="50" width="50"></a><div class="media-body"><div class="well well">'+grumbleText+'<span class="badge" style="float: right">'+dislikers.length+'</span></div>'+pic_block+'<ul class="list-group" id='+"comment-list-"+id+'></ul><div class="row" style="float:left"><div class="col-lg-12"><div class="input-group"><form class="form-inline" role="form" method = "post" onsubmit="return false"><div class="form-group"><input id = '+"comment-"+id+' type="text" name = "comment" class="form-control" placeholder="Write down your comments ..."></div><div class="form-group"><span class="input-group-btn"><button class="btn btn-primary" onclick = "foo('+id+","+user+')"><span class="glyphicon glyphicon-edit"></span> Comment</button></span></div></form></div></div></div><form role="form" method="post" action= "#"><input type="hidden" name = "dislike" class="form-control"><button class="btn btn-warning" type="button"><span class="glyphicon glyphicon-thumbs-down"></span> Dislike</button></form></div></div></div></div>'
		;
        list.insertBefore(newGrumble, list.childNodes[0]);
	}
}
if (window.location.href == "http://localhost:8000/grumblr/follower" || window.location.href == "http://localhost:8000/grumblr/")
{
    window.setInterval(sendRequest, 10000);
}


function bar(){
            foo(id,user);
        }

function foo(post_id,user_id, comment_id){
	console.log("ahello");
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({ 
     beforeSend: function(handleResponse, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             handleResponse.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
	});

	var text = document.getElementById("comment-"+post_id).value;
	req = $.ajax({
        url:'/grumblr/add-comment/' + post_id +'&'+ user_id,
        type: "POST",
        data: {text: text, post_id: post_id, user_id: user_id},
        success: function(){
            handleCommentResponse(post_id);
        },
    });
}
function handleCommentResponse(post_id) {
    var list = document.getElementById("comment-list-"+post_id);
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }

	var comments = JSON.parse(req.responseText);
    
    for (var i = 0; i < comments.length; ++i) {
        var text = comments[i]["fields"]["text"];
        var user = comments[i]["fields"]["commenter"];
        var user_name = comments[i]["fields"]["commenter_name"];
        var commentLi = document.createElement("li");
        commentLi.innerHTML = '<li class="list-group-item">'+text+'<span style="float:right">By '+user_name +'<a href = "#"></a></span></li>';
        list.appendChild(commentLi);
        }
}
