//# 데이터를 안보내고 그냥 페이지에서 java 스크립에서
var numcheck = "1번질문체크해주세요" ; 
var numcheck1 = "2번질문체크해주세요" ; 
var numcheck2 = "3번질문체크해주세요" ; 
var numcheck3 = "4번질문체크해주세요" ; 
var numcheck4 = "5번질문체크해주세요" ; 

function surveyCheck(){
	if ( ! surveyForm.num.value){
		alert(numcheck);
		
		return false;
	} else if( ! surveyForm.num1.value) {
		alert(numcheck1);
			
		return false;
	} else if ( ! surveyForm.num2.value){
		alert(numcheck2);
		return false;
	} else if( ! surveyForm.num3.value){
		alert(numcheck3);
		return false;
	} else if( ! surveyForm.num4.value){
		alert(numcheck4);	
		return false;
	} 
}






