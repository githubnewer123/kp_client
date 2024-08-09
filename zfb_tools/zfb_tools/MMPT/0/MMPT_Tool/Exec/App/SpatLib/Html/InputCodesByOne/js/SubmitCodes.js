function Submit(){
	for (var i=0; i<Settings.Barcodes.length; i++) {
		if (Settings.Barcodes[i].Enable) {
			//validate current barcode
			var ret = ValidateBarcode(i);
			if(ret != 0){
					$("#BarcodeError").html(ret);
					$("#" + Settings.Barcodes[i].Name).focus();
					$("#" + Settings.Barcodes[i].Name).select();
					return;
				}

			if(!ValidatePrefix(i)){
					$("#BarcodeError").html(Settings.Barcodes[i].Name + " prefix is  invalid!");
					$("#" + Settings.Barcodes[i].Name).focus();
					$("#" + Settings.Barcodes[i].Name).select();
					return;
				}
			}
		}

		var vInput = new Object();
		
		for(var i=0; i<Settings.Barcodes.length; i++){
			if(Settings.Barcodes[i].Enable){
				vInput[Settings.Barcodes[i].Name]=$("#"+Settings.Barcodes[i].Name).val();
			}
		
		}
		AppHelp.SaveJson(vInput);
		AppHelp.Submit();
}

$(function() {
	//Button click
	$("#apply").on("click", function() {
		Submit();
	});
});

