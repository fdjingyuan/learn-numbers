api_url = "http://127.0.0.1:5000/"
console.log("update_problem.js");

function update_problem() {
    var sym = RndSym();
    var num1 = RndNum();
    var num2 = RndNum();
    if(sym == '-') {
        while(num2 > num1 || num2 > 30 || num1 > 30){
            num1 = RndNum()
            num2 = RndNum()
        }
    }else{
        while(num2 > 30 || num1 > 30){
            num1 = RndNum()
            num2 = RndNum()
        }
    }
    if(sym == '+')
        $.result_math = num1 + num2
    else
        $.result_math = num1 - num2

    $('#num1').text(num1);
    $('#num2').text(num2);
    $('#symbol').text(sym);
    $('#equal').text("=");
    $('#right_answer_math').attr('value','');
    $('#recognize_text').attr('value','');
    $('#clear').trigger('click');
}

function get_result_math(){
    $('#right_answer_math').attr('disabled', 'false');
    $('#right_answer_math').attr('value',$.result_math);
    $('#right_answer_math').attr('disabled', 'ture');
}

function get_result_reading(){
    console.log($.result_reading)
    $('#right_answer_reading').attr('disabled', 'false');
    $('#right_answer_reading').attr('value',$.result_reading);
    $('#right_answer_reading').attr('disabled', 'ture');
}

function RndNum(){
    var rnd = Math.floor(Math.random()*49)+1;
    return rnd;
}

function RndSym() {
    var p = Math.random()
    if (p > 0.5)
        return '+'
    else
        return '-'
}





//  MATH:
//update problem
$(function(){
    $('#update_problem').click(function(){
        console.log("update");
        update_problem();
    })
     $('#submit_math').click(function(){
        console.log("submit_math");
        get_result_math();
        if ($("#recognize_text").attr("value") == $.result_math.toString())
            swal("Congratulations", "You are right!", "success");
        else
            swal("Wrong", "Please try again", "error")

    })

});




//Reading:
$(function() {
    $('#listen').click(function () {
        var num = RndNum();
        var string = num.toString();
        $.result_reading = num;
        var address = api_url + 'voice/' + string;
        $('#right_answer_reading').attr('value','');
        $('#recognize_text').attr('value','');
        $('#clear').trigger('click');
        $.ajax({
        url: address,
        type: "GET",
        success: function (msg) {
        }});
    });

    $('#submit_reading').click(function(){
    console.log("submit_reading");
        get_result_reading();
        if ($("#recognize_text").attr("value") == $.result_reading.toString())
            swal("Congratulations", "You are right!", "success");
        else
            swal("Wrong", "Please try again", "error")
    })
});



