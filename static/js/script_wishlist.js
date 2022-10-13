$(document).ready(
	function() { 
		$(".prodPrice").each( /* 배열관리할때 사용함, 매개 변수로 받은 것을 사용해 객체의 요소를 검사한다, ().each() 는 반복문과 비슷하다 */ 
			function(index, item) { /* 인덱스, item: 해당 선택자인 객체를 나타냄 this랑 같음 */
				const prodPriceElement = document.getElementsByClassName("prodPrice")[index]; /* 상품별로 가격을 인덱스화 */
				let prodPrice = parseInt(prodPriceElement.innerText.replace("원", "")); /* prodPriceElement에 문자열을 숫자로 반환하여 innertext 하고 바꾼다, 원이라고 있으면 빈 문자열로 힌디*/
				$($(".prodPrice")[index]).html(String(prodPrice).replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " 원"); /* 상품별 가격에 정규표현식을 사용하여 3번째마다 ,를 넣는다*/
			}
		);
		$("#goshopping").on(
			"click",
			function() {
				location.href = "/product/productCategory"; /* 쇼핑 계속하기를 누르면 상품 카테고리 페이지로 간다*/
			}
		);
		$("#delallwish").on(
			"click",
			function() {
				location.href = "/wishlist/wishdel?wishNum=0"; /* 찜 목록 비우기를 누르면 찜 목록이 초기화 된다*/
			}
		);
		$("#delwish").on(
			"click",
			function() {
				location.href = "/wishlist/wishdel?wishNum=0"; /* 여기는 지금 사용 안하는 중  */
			}
		);
	}
);