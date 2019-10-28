res_id=[];
function audioGo(message, method) {
    alert("The data is on the bottom!");
    $("#data").empty();
    res_id = [];

    var apigClient = apigClientFactory.newClient({
        apiKey: '5onPi5CAYe677kkTLLUQy8HNsgR5PSG88vXWIIuU'});
    var body={
    };
    var params={
        q: message
    };
    var additionalParams={
    };

    if(method=="Location"){
        apigClient.locationGet(params, body, additionalParams)
        .then(function(result){
            console.log(result);

            if(result["data"]["greeting"].length != 0){
                for (var i = 0; i < result["data"]["greeting"].length; ++i){
                    var info_res = result["data"]["greeting"][i];
                    res_id.push(info_res['id']);
                    var new_row = "<div class='col' id='"+i+"'>";
                    new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                    new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                    new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                    new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                    new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                    var temp_fea = info_res['feature'].split(",");
                    var feature="";
                    for(var j = 0; j < temp_fea.length;++j){
                        if(temp_fea[j] != ''){
                        feature += temp_fea[j] + "/";
                        }
                    }
                    new_row +="<div><b>Feature</b>:"+feature+"</div>";
                    new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                    new_row += "</div>";
                    $("#data").append(new_row);
                }
            }
            else{
                $("#data").append("No result Found!");
            }
        });

    }
    else if(method=="Name"){
        apigClient.nameGet(params, body, additionalParams).then(function(result){
            console.log(result);

            if(result["data"]["greeting"].length != 0){
                for (var i = 0; i < result["data"]["greeting"].length; ++i){
                    var info_res = result["data"]["greeting"][i];
                    res_id.push(info_res['id']);
                    var new_row = "<div class='col' id='"+i+"'>";
                    new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                    new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                    new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                    new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                    new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                    var temp_fea = info_res['feature'].split(",");
                    var feature="";
                    for(var j = 0; j < temp_fea.length;++j){
                        if(temp_fea[j] != ''){
                        feature += temp_fea[j] + "/";
                        }
                    }
                    new_row +="<div><b>Feature</b>:"+feature+"</div>";
                    new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                    new_row += "</div>";
                    $("#data").append(new_row);
                }
            }
            else{
                $("#data").append("No result Found!");
            }
        }).catch(function(result){

        });
    }
    else if(method=="Feature"){
        apigClient.featureGet(params, body, additionalParams)
        .then(function(result){
            console.log(result);

            if(result["data"]["greeting"].length != 0){
                for (var i = 0; i < result["data"]["greeting"].length; ++i){
                    var info_res = result["data"]["greeting"][i];
                    res_id.push(info_res['id']);
                    var new_row = "<div class='col' id='"+i+"'>";
                    new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                    new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                    new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                    new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                    new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                    var temp_fea = info_res['feature'].split(",");
                    var feature="";
                    for(var j = 0; j < temp_fea.length;++j){
                        if(temp_fea[j] != ''){
                        feature += temp_fea[j] + "/";
                        }
                    }
                    new_row +="<div><b>Feature</b>:"+feature+"</div>";
                    new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                    new_row += "</div>";
                    $("#data").append(new_row);
                }
            }
            else{
                $("#data").append("No result Found!");
            }
        });
    }
    else{
        apigClient.priceGet(params, body, additionalParams)
        .then(function(result){
            console.log(result);

            if(result["data"]["greeting"].length != 0){
                for (var i = 0; i < result["data"]["greeting"].length; ++i){
                    var info_res = result["data"]["greeting"][i];
                    res_id.push(info_res['id']);
                    var new_row = "<div class='col' id='"+i+"'>";
                    new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                    new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                    new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                    new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                    new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                    var temp_fea = info_res['feature'].split(",");
                    var feature="";
                    for(var j = 0; j < temp_fea.length;++j){
                        if(temp_fea[j] != ''){
                        feature += temp_fea[j] + "/";
                        }
                    }
                    new_row +="<div><b>Feature</b>:"+feature+"</div>";
                    new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                    new_row += "</div>";
                    $("#data").append(new_row);
                }
            }
            else{
                $("#data").append("No result Found!");
            }
        });
    }
};

var apigClient = apigClientFactory.newClient({
	apiKey: '5onPi5CAYe677kkTLLUQy8HNsgR5PSG88vXWIIuU'});
function newMessage() {
        $("#data").empty();
        res_id = [];
        let message = document.getElementById("searhc_input").value;
        let method = document.getElementById("inputOption").value;

        var apigClient = apigClientFactory.newClient({
            apiKey: '5onPi5CAYe677kkTLLUQy8HNsgR5PSG88vXWIIuU'});
        var body={
        };
        var params={
            q: message
        };
        var additionalParams={
        };

        if(method=="Location"){
            apigClient.locationGet(params, body, additionalParams)
            .then(function(result){
                console.log(result);

                if(result["data"]["greeting"].length != 0){
                    for (var i = 0; i < result["data"]["greeting"].length; ++i){
                        var info_res = result["data"]["greeting"][i];
                        res_id.push(info_res['id']);
                        var new_row = "<div class='col' id='"+i+"'>";
                        new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                        new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                        new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                        new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                        new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                        var temp_fea = info_res['feature'].split(",");
                        var feature="";
                        for(var j = 0; j < temp_fea.length;++j){
                            if(temp_fea[j] != ''){
                            feature += temp_fea[j] + "/";
                            }
                        }
                        new_row +="<div><b>Feature</b>:"+feature+"</div>";
                        new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                        new_row += "</div>";
                        $("#data").append(new_row);
                    }
                }
                else{
                    $("#data").append("No result Found!");
                }
            });

        }
        else if(method=="Name"){
            apigClient.nameGet(params, body, additionalParams).then(function(result){
                console.log(result);

                if(result["data"]["greeting"].length != 0){
                    for (var i = 0; i < result["data"]["greeting"].length; ++i){
                        var info_res = result["data"]["greeting"][i];
                        res_id.push(info_res['id']);
                        var new_row = "<div class='col' id='"+i+"'>";
                        new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                        new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                        new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                        new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                        new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                        var temp_fea = info_res['feature'].split(",");
                        var feature="";
                        for(var j = 0; j < temp_fea.length;++j){
                            if(temp_fea[j] != ''){
                            feature += temp_fea[j] + "/";
                            }
                        }
                        new_row +="<div><b>Feature</b>:"+feature+"</div>";
                        new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                        new_row += "</div>";
                        $("#data").append(new_row);
                    }
                }
                else{
                    $("#data").append("No result Found!");
                }
            }).catch(function(result){

            });
        }
        else if(method=="Feature"){
            apigClient.featureGet(params, body, additionalParams)
            .then(function(result){
                console.log(result);

                if(result["data"]["greeting"].length != 0){
                    for (var i = 0; i < result["data"]["greeting"].length; ++i){
                        var info_res = result["data"]["greeting"][i];
                        res_id.push(info_res['id']);
                        var new_row = "<div class='col' id='"+i+"'>";
                        new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                        new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                        new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                        new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                        new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                        var temp_fea = info_res['feature'].split(",");
                        var feature="";
                        for(var j = 0; j < temp_fea.length;++j){
                            if(temp_fea[j] != ''){
                            feature += temp_fea[j] + "/";
                            }
                        }
                        new_row +="<div><b>Feature</b>:"+feature+"</div>";
                        new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                        new_row += "</div>";
                        $("#data").append(new_row);
                    }
                }
                else{
                    $("#data").append("No result Found!");
                }
            });
        }
        else if(method=="Category"){
            apigClient.categoryGet(params, body, additionalParams)
            .then(function(result){
                console.log(result);

                if(result["data"]["greeting"].length != 0){
                    for (var i = 0; i < result["data"]["greeting"].length; ++i){
                        var info_res = result["data"]["greeting"][i];
                        res_id.push(info_res['id']);
                        var new_row = "<div class='col' id='"+i+"'>";
                        new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                        new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                        new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                        new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                        new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                        var temp_fea = info_res['feature'].split(",");
                        var feature="";
                        for(var j = 0; j < temp_fea.length;++j){
                            if(temp_fea[j] != ''){
                            feature += temp_fea[j] + "/";
                            }
                        }
                        new_row +="<div><b>Feature</b>:"+feature+"</div>";
                        new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                        new_row += "</div>";
                        $("#data").append(new_row);
                    }
                }
                else{
                    $("#data").append("No result Found!");
                }
            });
        }
        else{
            apigClient.priceGet(params, body, additionalParams)
            .then(function(result){
                console.log(result);

                if(result["data"]["greeting"].length != 0){
                    for (var i = 0; i < result["data"]["greeting"].length; ++i){
                        var info_res = result["data"]["greeting"][i];
                        res_id.push(info_res['id']);
                        var new_row = "<div class='col' id='"+i+"'>";
                        new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                        new_row +="<div><b>Cuisine</b>:"+info_res['category']+"</div>";
                        new_row +="<div><b>Rating</b>:"+info_res['rating']+"</div>";
                        new_row +="<div><b>Price</b>:"+info_res['price']+"</div>";
                        new_row +="<div><b>Location</b>:"+info_res['location']+"</div>";
                        var temp_fea = info_res['feature'].split(",");
                        var feature="";
                        for(var j = 0; j < temp_fea.length;++j){
                            if(temp_fea[j] != ''){
                            feature += temp_fea[j] + "/";
                            }
                        }
                        new_row +="<div><b>Feature</b>:"+feature+"</div>";
                        new_row += "<img src='"+info_res["image_url"]+"' height=100 width=100>";
                        new_row += "</div>";
                        $("#data").append(new_row);
                    }
                }
                else{
                    $("#data").append("No result Found!");
                }
            });
        }
};

$(document).ready(function() {
    $("#trans").click(function(){
        var trans_text="";
        for(var i = 0; i < res_id.length; ++i){

            var tmp_text = $("#"+i+"name").text();

            trans_text += tmp_text.substring(6,tmp_text.length)+",";
        }
        trans_text = trans_text.substring(0, trans_text.length - 1);
        var body={
            "message":{
                    "word":trans_text
            }
        };
        var params={};
        var additionalParams={};
        //var apigClient = apigClientFactory.newClient({
         //   apiKey: '5onPi5CAYe677kkTLLUQy8HNsgR5PSG88vXWIIuU'});

        apigClient.translatePost(params, body, additionalParams)
        .then(function(result){
            // Add success callback code here.
            var return_bot = result["data"]["greeting"];
            for(var i = 0; i < return_bot.length; ++i){
                $("#"+i+"name").text("Name: "+return_bot[i]);
            }
        }).catch( function(result){
            // Add error callback code here.
            console.log("the return method is wrong!");
        });
    });
    $("#num").click(function(){
        var id_text="";
        for(var i = 0; i < res_id.length; ++i){
            id_text += res_id[i] +',';
        }
        id_text = id_text.substring(0, id_text.length - 1);
        var body={
            "message":{
                    "word":id_text
            }
        };
        var params={};
        var additionalParams={};
        var apigClient = apigClientFactory.newClient({
            apiKey: '5onPi5CAYe677kkTLLUQy8HNsgR5PSG88vXWIIuU'});

        apigClient.numberPost(params, body, additionalParams)
        .then(function(result){
            // Add success callback code here.
            var return_bot = result["data"]["greeting"];
            for(var i = 0; i < return_bot.length; ++i){
                $("#"+i).append("<div>Current People: "+return_bot[i]["count"]+"</div>");
            }
        }).catch( function(result){
            // Add error callback code here.
            console.log("the return method is wrong!");
        });
    });
});


function uploadPhoto(){
		document.getElementById("progressBar").hidden = false;
		var file = document.getElementById("file-upload").files[0];

		if (file){
			console.log(file.name);
			var preview = document.querySelector('img');
			var file_name = file.name;
	    	var file_type = file.type;
	    	var file_src = preview.src;
	    	file_src = file_src.replace('data:image/jpeg;base64,','');
	    	console.log(typeof(file_src))
			if (!file.type.match('image.*')){
				alert("Please upload an image");
				return false;
			}
			console.log(file)

			var params = {};
			var body = {data : file_src}

			var additionalParams = {};
            $("#data").empty();
			apigClient.imgsearchPost(params, body, additionalParams)
				.then(function(result){
					if(result["data"]["greeting"].length != 0){
                        for (var i = 0; i < result["data"]["greeting"].length; ++i){
                            var info_res = result["data"]["greeting"][i];
                            var new_row = "<div class='col' id='"+i+"'>";
                            var food_id = info_res['id'];
                            new_row +="<div id='"+i+"name'><b>Name</b>: "+info_res['name']+"</div>";
                            new_row +="<div><b>Cuisine</b>:"+info_res['cuisine']+"</div>";
                            new_row +="<img src='https://s3.amazonaws.com/couldcomputingfood/img"+food_id+".jpg' height=150 width=150>";
                            new_row += "<audio controls>";
                            new_row += '<source src="https://s3.amazonaws.com/cc-project-2019sp/'+food_id+'.mp3" type="audio/mpeg">';
                            new_row += "</audio>";
                            new_row += "</div>";
                            $("#data").append(new_row);
                        }
                    }
                    else{
                        $("#data").append("No result Found!");
                    }
				}).catch(function(result){
					console.log("[error] catch error in response.");
				});
		} else{
			alert("Select a photo!");
		}
}

function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

function previewFile() {
    var preview = document.querySelector('img');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();

    reader.addEventListener("load", function () {
        preview.src = encode_utf8(reader.result);
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}

function UploadPPhoto(){
    var preview = document.querySelector('img');
    var file = document.querySelector('input[type=file]').files[0];
    var file_name = file.name;
    var file_type = file.type;
    var file_src = preview.src;
    file_src = file_src.replace('data:image/jpeg;base64,','');
    console.log(file_name);
    console.log(file_src);
    console.log(file_type);
    console.log(file);
    //sdk.uploadPut({bucket: 'assignmen-3-b2', photo: file_name, 'Content-Type': file_type}, file_src, {});
}
