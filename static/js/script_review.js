/**
 * 
 */

function writereview(prodNum, prodName) {
	document.reviewform.prodNum.value = prodNum;
	document.reviewform.prodName.value = prodName;
}


function modifyreview(reviewNum, reviewTitle){
	document.reviewform.reviewNum.value = reviewNum;
	document.reviewform.reviewTitle.value = reviewTitle;
}

function deletereview(reviewNum){
	reviewdelete.reviewNum.value = reviewNum;
}

function reviewcheck(){
	if(! reviewform.reviewTitle.value){
		alert("제목을 입력하세요.")
		reviewform.reviewTitle.focus();
		return false;
	}
	else if(! reviewform.reviewContent.value){
		alert("내용을 입력하세요.")
		reviewform.reviewContent.focus();
		return false;
	}
}