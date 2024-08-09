/**
 * Created by Administrator on 2016/8/30.
 */

function GetImei15(Digit){
	var DigitLength = 14;
	var Sum = new Number(0);
	for(var i=0; i<DigitLength; i++){
		var x1 = new Number(Digit.substring(i, i+1));
		i++;
		var temp = new Number(Digit.substring(i, i+1)) * 2;
		var x2 = temp<10? temp: temp%10 + parseInt(temp/10);
		Sum += x1+x2;
	}
	Sum %= 10;
	Sum = Sum==0? 0: 10 - Sum;
	
	return Sum;
}

function Get15thOfMEID(meid){
	var sum = 0;
	for(var i=0; i<14;){
		var  odd = parseInt(meid.substring(i, i+1), 16);
		i++;
		var even = parseInt(meid.substring(i, i+1), 16) * 2;
		sum += (odd + (((even&0xF0) >> 4) + (even&0x0F)));
		i++;
	}
	if ((sum % 16) == 0) {
		return '0';
	} else {
		var chksum = 16 - (sum % 16);
		return chksum.toString(16).toUpperCase();
	}
}

function VerifyInputCode(index) {

	if (Settings.Codes[index].CodeType == "QRCode") {
		// QR code valid verification
		var   label = Settings.Codes[index].Label;
		var   input = $("#" + label).val();
		var exp_len = Settings.Codes[index].Length;

		if (Settings.Codes[index].Format == "V1") {
			/*
				V1 format: Key1=Value1;Key2=Value2;...  
				Example: IMEI1=11111111111;IMEI2=222222222222
			*/
			if (!VerifyQRCodeV1(label, exp_len)) {
				$("#" + label).focus();
				$("#" + label).select();
				return false;
			}
		}
		else if (Settings.Codes[index].Format == "V2") {
			/*
				V2: IMEI;SN
				Example: 86486702999650;2009117T0102N0000001
			*/
			if (!VerifyQRCodeV2(input, exp_len)) {
				$("#" + label).focus();
				$("#" + label).select();
				return false;
			}
		}
		else if (Settings.Codes[index].Format == "V3") {
			/*
				V3: Bug1189339
				sprintf(param, "%s[,-]%s[,-]%d", sn, ipAddr, port)
				以逗号分隔,sn, ipaddr, port
			*/
			if (!VerifyQRCodeV3(input)) {
				$("#BarcodeError").html("Invalid QRCode, should be sn[,-]ip[,-]port!");
				$("#" + label).focus();
				$("#" + label).select();
				return false;
			}
		}
		else if (Settings.Codes[index].Format == "V4") {
			/*
			自定义Customize
			*/
			var input_len = $("#" + label).val().length;
			if (input_len != exp_len) {
				$("#BarcodeError").html("Input length is " + input_len.toString() + " not equal to " + exp_len.toString());
				$("#" + label).focus();
				$("#" + label).select();
				return false;
			}
		}	
		else {
			$("#BarcodeError").html("Unknown QR format!");
			$("#" + label).focus();
			$("#" + label).select();
			return false;
		}
	}
	
	return true;
}

 function VerifyQRCodeV1(label, exp_len) {
	/*
		V1 format: Key1=Value1;Key2=Value2;...  
		Example: IMEI1=11111111111;IMEI2=222222222222
	*/
	// Check input length 
	
	if(-1== $("#" + label).val().search(/=/g)){
		$("#BarcodeError").html("Input format is wrong!");
		return false;
	}
	
	var strItems = new Array(); 
	strItems = $("#" + label).val().split(";");
	var strVar = new Array();
	for (i=0; i<strItems.length; i++ ) 
	{ 
		strvar = [];
		strvar = strItems[i].split("=");
		if(-1 != strvar[0].search(/IMEI/g)){
			if(strvar[1].length != 15){
				$("#BarcodeError").html(strvar[0] + " length != 15!");
				return false;
			}
			var digit = strvar[1].substring(0, 14);
			var sum   = strvar[1].substring(14,15);
			if (parseInt(sum, 10) != GetImei15(digit)) {
				$("#BarcodeError").html("The 15th " + strvar[0] + " checksum fail!");
				return false;
			}
		}
		else if(-1!= strvar[0].search(/WIFI/g)){
			if(strvar[1].length != 12){
				$("#BarcodeError").html(strvar[0] + " length != 12!");
				return false;
			}		
			var szTemp = strvar[1].substring(1,2);
			var nTemp = parseInt(szTemp, 16);
			if((nTemp != 4) && (nTemp != 8) && (nTemp != 0xC) && (nTemp != 0)){
				$("#BarcodeError").html(strvar[0] + " 111 1st byte of must be even number!");
				return false;
			}
		}
		else if(-1!= strvar[0].search(/MEID/g)){
			if(strvar[1].length == 15){
				var meid  = strvar[1].substring(0, 14);
				var the15 = strvar[1].substring(14,15);
				if(the15 != Get15thOfMEID(meid)){
					$("#BarcodeError").html(strvar[0] + " check sum fail!");
					return false;
				}
			}
			else if(strvar[1].length == 14){
				var meid  = strvar[1] + Get15thOfMEID(strvar[1]);
				var str = $("#" + label).val().replace("MEID="+strvar[1], "MEID="+meid);
				$("#" + label).val(str);
			}
			else{
				$("#BarcodeError").html(strvar[0] + " length is wrong!");
				return false;
			}		
			
		}
		else if(-1!= strvar[0].search(/BT/g)){
			if(strvar[1].length != 12){
				$("#BarcodeError").html(strvar[0] + " length != 12!");
				return false;
			}			
		}
	} 
	
	if (exp_len > 0) { 
		var input_len = $("#" + label).val().length;
		if (input_len != length) {
			$("#BarcodeError").html("Input length is " + input_len.toString() + " not equal to " + exp_len.toString());
			return false;
		}
	}
	
	// TODO: Add extra verify code here 
	
	return true;
}


 function VerifyQRCodeV2(input, exp_len) {
	 /*
        V2: IMEI;SN
        Example: 86486702999650;2009117T0102N0000001
	 */
	if (-1 == input.search(/;/g)) {
		$("#BarcodeError").html("Invalid QRCode, the format should be IMEI;SN!");
		return false;
	}
	
	var arrCodes = new Array(); 
	arrCodes = input.split(";");

	// IMEI
	if (arrCodes[0].length < 14 || arrCodes[0].length > 15) {
		$("#BarcodeError").html("Invalid IMEI length");
		return false;
	}
	
	if (arrCodes[0].length == 15) {
		var digit = arrCodes[0].substring(0, 14);
		var sum   = arrCodes[0].substring(14,15);
		if (parseInt(sum, 10) != GetImei15(digit)) {
			$("#BarcodeError").html("The 15th IMEI checksum fail!");
			return false;
		}
	}
	
	return true;
 }
 
 function checkIP(ip) {
    var exp=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    return exp.test(ip);
}

function checkDigital(value) {
	var exp=/^[0-9]*$/;
    return exp.test(value);
}
 
 function VerifyQRCodeV3(input) {
	/*
		V3: Bug1189339
		sprintf(param, "%s[,-]%s[,-]%d", sn, ipAddr, port)
		以逗号分隔,sn, ipaddr, port
	*/
	var arrCodes = new Array(); 
	arrCodes = input.split(/[,-]/);
	if ((arrCodes.length != 3) || (!checkIP(arrCodes[1])) || (!checkDigital(arrCodes[2]))) {
		return false;
	}

	return true;
 }
 
$(function() {
	//Enter Key event
    $(".BarcodeInputBox").keyup(function (event) {
		var eve = event||window.event;
		if (eve.keyCode == 13/*EnterKey*/) {
			// Check from current code
			var index = Number($(this).attr("index"));
			do {
					if (!VerifyInputCode(index)) {
						return;
					}
			
			
					// Check next code
					++index;
				
					if (index == Settings.Codes.length) {
						// reach the last one, then submit
						$("#apply").click();
						return;
					}
				
					// If next code is ScanCode, wait to input code
					if (Settings.Codes[index].Enable && Settings.Codes[index].GenerateType == "ScanCode"){
						// Skip to next ScanCode to wait input
						$("#" + Settings.Codes[index].Label).focus();
						$("#" + Settings.Codes[index].Label).select();
						return;
					}
			} while (index <= Settings.Codes.length);
		}
		else {
			if ($(this).val().length > 0) {
				$("#BarcodeError").html("");
			}
		}
    });
});


