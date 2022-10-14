$(document).ready(
	function () {

		$(".prodStock").each(
			function(index, item){		// 재고의 값을 정수화 시켜 구매 수량보다 크면 table-warning 태그를 추가한다
				if(parseInt($(item).val()) < parseInt($($(".buyCount")[index]).val())){
					$($(".cart_row")[index]).addClass("table-warning");
				}
			}
		);
		
		// 이벤트 처리
	    $("#goshopping").on(
            "click",
            function() {
                location.href = "/product/productCategory";		// 카테고리 페이지로 이동
            }
        );
	    $("#delcartall").on(
            "click",
            function() {
                location.href = "/cart/cartdel?cartNum=0";		//	카트 번호를 초기화 시킨다, 장바구니를 비운다
            }
        );
	    $("#order").on(
            "click",
            function() {	// 카트의 길이가 0일 때 비어 있다는 메세지를 출력하고 주문을 실패한다
            	if ($(".cart_row").length == "0"){			
            		alert("장바구니가 비어있습니다.");
            		return false;
            	}
            	if($(".table-warning").length > 0)			// 0보다 구매 수량이 많을 떄
            		alert("현재 장바구니의 상품 중 수량이 현재 재고를 넘는 것이 있습니다.\n상품 수량을 다시 선택해주세요.");
            	else									// 0보다 적거나 같을 때 , 결제 페이지로 이동함
                    location.href = "/order/order";		
            }
        );
    }
);
/* cart.html에서 받은 것 */
function modCart(cartNum, index){
	let buyCountElement = document.getElementsByClassName("buyCount")[index];	/* 구매 수량을 인덱스시킴 */
	let buyCount = buyCountElement.value;	/* value로 지정 */
	if (buyCount <= 0){		/* 재고가 0이나 음수일 경우 알림과 포커스를 준다 실패로 되돌린다 */
		alert("0 또는 음수가 올 수 없습니다.")
		buyCountElement.focus;
		return false;
	}
	location.href = "/cart/cartmod?cartNum=" + cartNum + "&buyCount=" + buyCount;	/* 카트 번호와 구매수량을 주소화시킴*/
}