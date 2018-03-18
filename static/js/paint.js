api_url = "http://127.0.0.1:5000/"

function clearCanvas()
{
    var c=document.getElementById("canvas");
    var cxt = c.getContext("2d");
    cxt.clearRect(0,0,c.width,c.height);
}


$(function(){
    $('#clear').click(function(){
        clearCanvas();
    })
});


function convertCanvasToImage() {
	var image = new Image();
	var c=document.getElementById("canvas");
	image.src = c.toDataURL("image/png");
	return image.src.substr(22, image.src.length)
}

$(function(){
    $('#recognize').click(function(){
        var img = convertCanvasToImage();
        $.ajax({
        url: api_url + "recognize/",
        type: "POST",
        data: img,
        dataType : "json",
        success: function (msg) {
            console.log(msg);
            $.tt = msg
            // var j = eval(msg);
            if (msg.status == 'success'){
                $('#recognize_text').attr('value', msg.data);
            }else{
                alert(msg.data);
            }
        }
    })
    })
});
