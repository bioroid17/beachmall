$(document).ready(
	function () {

		$(".prodStock").each(
			function(index, item){
				if(parseInt($(item).val()) < parseInt($($(".buyCount")[index]).val())){
					$($(".cart_row")[index]).addClass("table-warning");
				}
			}
		);
		
		// 이벤트 처리
	    $("#goshopping").on(
            "click",
            function() {
                location.href = "/product/productCategory";
            }
        );
	    $("#delcartall").on(
            "click",
            function() {
                location.href = "/cart/cartdel?cartNum=0";
            }
        );
	    $("#order").on(
            "click",
            function() {
            	if ("{{carts|length}}" == "0"){
            		alert("장바구니가 비어있습니다.");
            		return false;
            	}
            	if($(".table-warning").length > 0)
            		alert("현재 장바구니의 상품 중 수량이 현재 재고를 넘는 것이 있습니다.\n상품 수량을 다시 선택해주세요.");
            	else
                    location.href = "/order/order";
            }
        );
    }
);
function modCart(cartNum, index){
	let buyCountElement = document.getElementsByClassName("buyCount")[index];
	let buyCount = buyCountElement.value;
	if (buyCount <= 0){
		alert("0 또는 음수가 올 수 없습니다.")
		buyCountElement.focus;
		return false;
	}
	location.href = "/cart/cartmod?cartNum=" + cartNum + "&buyCount=" + buyCount;
}