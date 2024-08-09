function Submit() {
	for (var i=0; i<Settings.Codes.length; i++) {
		if (Settings.Codes[i].Enable) {
			if (!VerifyInputCode(i)) {
				return;
			}
		}
	}

	var json = {};
	for(var i=0; i<Settings.Codes.length; i++){
		if(Settings.Codes[i].Enable){
			if (Settings.Codes[i].CodeType == "QRCode") {
				var QR = {};
				if (Settings.Codes[i].Format == "V2") {
					var arrCodes = new Array(); 
					arrCodes = $("#" + Settings.Codes[i].Label).val().split(";");
					if (arrCodes[0].length == 14) {
						// fill the 15 chksum
						var chksum = GetImei15(arrCodes[0].substring(0, 14)).toString();
						QR["Code"] = arrCodes[0] + chksum + ";" + arrCodes[1];
					} else {
						QR["Code"] = $("#"+Settings.Codes[i].Label).val();
					}
				} else {
					QR["Code"] = $("#"+Settings.Codes[i].Label).val();
				}
				QR["Format"] = Settings.Codes[i].Format;
				json[Settings.Codes[i].Label] = QR;
				
			} else {
				json[Settings.Codes[i].Label] = $("#"+Settings.Codes[i].Label).val();
			}
			
			if (debug.DEBUG_IN_BROWSER) {
				console.log(QR);
			}
		}
	}
	
	AppHelp.SaveJson(json);
	AppHelp.Submit();
}

$(function() {
	//Button click
	$("#apply").on("click", function() {
		Submit();
	});
});

