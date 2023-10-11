let isAuto = true;

$(function() {
    showState();
    
    // 自動・各個　切り替え
    $("#swAuto").on('click', function(){
        isAuto = !isAuto;
        showState();
        showLED();
    })

    // ランプ全点灯ボタンを押す
    $("#btnAllLight").mousedown(function(){
        if (! isAuto) {
            $("#imgLight").attr("src", "static/images/btn_push.png");
            for (i=0; i<5; i++){
                $("#lamp" + i).css("color","red");
                $("#lamp_led").css("color","red");
            }
        }
    })

    // ランプ全点灯ボタンを離す
    $("#btnAllLight").mouseup(function(){
        if (! isAuto) {
            $("#imgLight").attr("src", "static/images/btn_normal.png");
            showLamps();
            showLED();
        }
    })

    // LED強制点灯ボタンを押す
    $("#btnLedOn").mousedown(function(){
        if (! isAuto) {
            $("#btnLedOn").attr("src", "static/images/btn_push.png");
            $("#imgLed").attr("src", "static/images/led_on.png");
            $("#lamp_led").css("color", "red");
        }
    })

    // LED強制点灯ボタンを離す
    $("#btnLedOn").mouseup(function(){
        if (! isAuto) {
            $("#btnLedOn").attr("src", "static/images/btn_normal.png");
            $("#imgLed").attr("src", "static/images/led_off.png");
            showLED();
        }
    })

    // トライボタン切り替え
    $(".btnTry").on('click', function(){
        isTry = !isTry;
        showTry();
    })
})


// フラグの状態を表示する関数
function showState() {
    var strAuto = "";
    var imgSw = "";
    if (isAuto) {
        strAuto = "自動";
        imgSw = "sw_l.png";
    } else {
        strAuto = "各個";
        imgSw = "sw_r.png";
    };
    $("#stateAuto").text(strAuto);
    $("#imgAuto").attr("src", "static/images/" + imgSw );
}

// 光センサーの状態を表示する関数
function showLamps() {
    $.each(lamps,function(index,val){
        var color="";
        if (val) {
            color = "red";
        } else {
            color = "gray";
        }
        $("#lamp" + index).css("color",color);
    });
}

// 育成LEDをの状態を表示する関数
function showLED() {
    var color="";
    if (isLED) {
        color = "red";
    } else {
        color = "gray";
    }
    $("#lamp_led").css("color",color);
}