/**
 * Created by Administrator on 2016/8/26.
 */

var AppHelp = (function () {
/*
    var debug = {
            DEBUG_IN_BROWSER : false
    }
*/
    function Submit() {
        if (debug.DEBUG_IN_BROWSER) {
            alert("Submit OK");
        }
        else {
            window.external.Submit();
        }
    }

    function SaveJson(obj) {
        if (debug.DEBUG_IN_BROWSER) {
            console.log("SaveJson");
        }
        else {
            var json = JSON.stringify(obj);
            window.external.SaveJson(json);
        }
    }

    function LoadJson() {
        if (debug.DEBUG_IN_BROWSER) {
            console.log("LoadJson");
        }
        else {
            var json = window.external.LoadJson();
            return eval("(" + json + ")");
        }
    }

    return {
        SaveJson : SaveJson,
        LoadJson : LoadJson,
        Submit   : Submit
    }
})();


