/**
 * Created by Administrator on 2016/8/30.
 */
var Settings = new Object();

function Init() {
    for (var i=0; i<2; i++) {
        $("#SN"+ (i + 1)).attr("disabled", !Settings.SN[i].Enable);
        $("#SN"+ (i + 1)).attr("maxlength", Settings.SN[i].MaxLength);
    }

    if (!Settings.SN[0].Enable && !Settings.SN[1].Enable) {
        $("#apply").attr("disabled", true);
    }
}

function validateInput(obj, len) {
    return ($("#"+obj).val().length == len) ? true : false;
}

$(function() {
    Settings = AppHelp.LoadJson();
    Init();

    $("input[type=text]").keyup(function () {
        if ($(this).val().length > 0) {
            $(this).val($(this).val().replace(/[^\w]|_/ig,''));
            $("#"+ $(this).attr("id")+"Span").html("");
        }
    });

    $("#apply").on("click", function () {
        for (var i=0; i<2; i++) {
            if (Settings.SN[i].Enable && !validateInput("SN"+ (i + 1), Settings.SN[i].MaxLength)) {
                $("#SN" + (i + 1) + "Span").html("Input SN is invalid!");
                return ;
            }
        }

        var vInput = new Object();
        vInput.SN1 = $("#SN1").val();
        vInput.SN2 = $("#SN2").val();
        AppHelp.SaveJson(vInput);
        AppHelp.Submit();
    });
});