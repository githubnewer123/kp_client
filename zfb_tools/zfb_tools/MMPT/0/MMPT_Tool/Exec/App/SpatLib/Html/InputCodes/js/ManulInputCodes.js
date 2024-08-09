/**
 * Created by Administrator on 2016/8/30.
 */


function Format(obj){
	var strName = $(obj).attr("Name");
	if(-1 != strName.search(/OTTSN/g))
	{
		$(obj).val($(obj).val().replace(/[^0-9|^a-f|^A-F]/g,''));
	}
	else if(-1 != strName.search(/SN/g)){
		$(obj).val($(obj).val().replace(/\W|_/g,''));
	}
	else if(-1 != strName.search(/IMEI/g)){
		$(obj).val($(obj).val().replace(/\D/g,''));
	}
	else if(-1 != strName.search(/WIFI/g) || -1 != strName.search(/BT/g)){
		$(obj).val($(obj).val().replace(/[^0-9|^a-f|^A-F]/g,''));
	}
	else if(-1 != strName.search(/MEID/g)) {
		$(obj).val($(obj).val().replace(/[^0-9|^a-f|^A-F]/g,''));
		$(obj).val($(obj).val().toUpperCase())
	}
	else if(-1 != strName.search(/ENETMAC/g)){
		$(obj).val($(obj).val().replace(/[^0-9|^a-f|^A-F]/g,''));
	}	
}

 function validateInputLength(obj, len) {
 	var strName =$("#"+obj).attr("Name");
 	if(-1 != strName.search(/SN/g) && -1 == strName.search(/OTTSN/g)){
 		return ($("#"+obj).val().length <= len) ? true : false;
 	}
 	else{
 		return ($("#"+obj).val().length == len) ? true : false;
 	}
}

function ValidateBarcode(sort){
	if("" != Settings.Barcodes[sort].Validation){		
		//var strValidation = Settings.Barcodes[sort].Validation.replace(/\\/g,"\\");
		var strValidation = Settings.Barcodes[sort].Validation;
		var strArray = strValidation.split(";");
		for(var i=0; i<strArray.length; i++){
			if("" != strArray[i])
			{
				var Validation = eval(strArray[i]);
				if(!Validation.test($("#" + Settings.Barcodes[sort].Name).val())){
					return Settings.Barcodes[sort].Name + " check " + strArray[i] + " fail!";
				}
			}
		}
	}
	
	if(-1 != Settings.Barcodes[sort].Name.search(/MEID/g)){
		if ($("#" + Settings.Barcodes[sort].Name).val().length == 14){
			var meid  = $("#" + Settings.Barcodes[sort].Name).val().substring(0, 14);
			$("#" + Settings.Barcodes[sort].Name).val(meid + Get15thOfMEID(meid));
			}
		}
	
	if(-1 != Settings.Barcodes[sort].Name.search(/SN/g) && -1 == Settings.Barcodes[sort].Name.search(/OTTSN/g)){
 		if ($("#" + Settings.Barcodes[sort].Name).val().length > Settings.Barcodes[sort].MaxLength){
			return Settings.Barcodes[sort].Name + " length > " + Settings.Barcodes[sort].MaxLength.toString() ;
		}
 	}
 	else{
 		if ($("#" + Settings.Barcodes[sort].Name).val().length != Settings.Barcodes[sort].MaxLength){
			return Settings.Barcodes[sort].Name + " length != " + Settings.Barcodes[sort].MaxLength.toString() ;
		}
 	}
 			
	//
	if(-1 != Settings.Barcodes[sort].Name.search(/IMEI/g)){
		if (Settings.Barcodes[sort].EnableInputCheck){
			var digit = $("#" + Settings.Barcodes[sort].Name).val().substring(0,14);
			var sum = $("#" + Settings.Barcodes[sort].Name).val().substring(14,15);
			if(parseInt(sum,10) != GetImei15(digit)){
				return Settings.Barcodes[sort].Name + " check sum fail!"
			}
		}
	}
	else if(-1!= Settings.Barcodes[sort].Name.search(/WIFI/g)){
		
			var szTemp = $("#" + Settings.Barcodes[sort].Name).val().substring(1,2);
			var nTemp = parseInt(szTemp, 16);
			if((nTemp != 4) && (nTemp != 8) && (nTemp != 0xC) && (nTemp != 0)){
				return Settings.Barcodes[sort].Name + " 111 1st byte of must be even number!"

		}
	}
	else if(-1 != Settings.Barcodes[sort].Name.search(/MEID/g)){
		if (Settings.Barcodes[sort].EnableInputCheck){
			var meid  = $("#" + Settings.Barcodes[sort].Name).val().substring(0, 14);
			var the15 = $("#" + Settings.Barcodes[sort].Name).val().substring(14,15);
			if(the15 != Get15thOfMEID(meid)){
				return Settings.Barcodes[sort].Name + " check sum fail!"
			}
		}
	}
	else 
	{
		if ($("#" + Settings.Barcodes[sort].Name).val().length <= 0){
		return Settings.Barcodes[sort].Name + " please input barcode";
		}
	}
	
	return 0;
}

function ValidatePrefix(sort){
	if("" != Settings.Barcodes[sort].Prefix){
		//var strValidation = Settings.Barcodes[sort].Validation.replace(/\\/g,"\\");
		var strValidation = "/^" + Settings.Barcodes[sort].Prefix +"/g";
		var Validation = eval(strValidation);
		if(!Validation.test($("#" + Settings.Barcodes[sort].Name).val())){
			return false;
		}
	}
	return true;
}


$(function() {
	//Enter Key event
    $(".BarcodeInputBox").keyup(function (event) {
		var eve = event||window.event;
		if(eve.keyCode == 13){
			var sort = Number($(this).attr("sort"));
			
			if(-1 != Settings.Barcodes[sort].Name.search(/MEID/g)){
		if ($("#" + Settings.Barcodes[sort].Name).val().length == 14){
			var meid  = $("#" + Settings.Barcodes[sort].Name).val().substring(0, 14);
			$("#" + Settings.Barcodes[sort].Name).val(meid + Get15thOfMEID(meid));
			}
		}
			
			//check length
			if(!validateInputLength(Settings.Barcodes[sort].Name, Settings.Barcodes[sort].MaxLength)){
				$("#BarcodeError").html(Settings.Barcodes[sort].Name + " length > " + Settings.Barcodes[sort].MaxLength.toString());
				$("#" + Settings.Barcodes[sort].Name).focus();
				$("#" + Settings.Barcodes[sort].Name).select();
				return;
			}
			
			//validate current barcode
			var ret = ValidateBarcode(sort);
			if(ret != 0){
				$("#BarcodeError").html(ret);
				$("#" + Settings.Barcodes[sort].Name).focus();
				$("#" + Settings.Barcodes[sort].Name).select();
				return;
			}
			
			if(!ValidatePrefix(sort)){
				$("#BarcodeError").html(Settings.Barcodes[sort].Name + " prefix is  invalid!");
				$("#" + Settings.Barcodes[sort].Name).focus();
				$("#" + Settings.Barcodes[sort].Name).select();
				return;
			}
			
			//if validate current barcode pass, then focus to next barcode
			sort++;
			do{
				if(sort == Settings.Barcodes.length){
					$("#apply").click();
					return;
				}
				
				if(Settings.Barcodes[sort].Enable && Settings.Barcodes[sort].GenerateType == "ManualInput"){
					$("#" + Settings.Barcodes[sort].Name).focus();
					$("#" + Settings.Barcodes[sort].Name).select();
					return;
				}
				else{
					sort++;
				}
			}
			while(sort <= Settings.Barcodes.length)
			
			//$("#" + Settings.Barcodes[sort+1].Name).focus();
			//keycode为13是Enter键 9是Tab键
		}
		else if(eve.keyCode == 9){ 
		}
		else{
			if ($(this).val().length > 0) {
				Format(this);
				$("#BarcodeError").html("");
			}
		}
    });
});


