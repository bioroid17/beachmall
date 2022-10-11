$(document).ready(
	function() {
		$(".prodPrice").each(
			function(index, item) {
				const prodPriceElement = document.getElementsByClassName("prodPrice")[index];
				let prodPrice = parseInt(prodPriceElement.innerText.replace("원", ""));
				$($(".prodPrice")[index]).html(String(prodPrice).replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " 원");
			}
		);
		$("#goshopping").on(
			"click",
			function() {
				location.href = "/product/productCategory";
			}
		);
		$("#delallwish").on(
			"click",
			function() {
				location.href = "/wishlist/wishdel?wishNum=0";
			}
		);
		$("#delwish").on(
			"click",
			function() {
				location.href = "/wishlist/wishdel?wishNum=0";
			}
		);
	}
);