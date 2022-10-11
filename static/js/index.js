// $("li").click(function () {
//   if ($(this).hasClass("active")) {
//     $(this).children().css("display", "none");
//     $(this).removeClass();
//   } else {
//     $(this).addClass("active");
//     $(this).children().css("display", "block");
//   }
// });

// $(document).ready(function(){

// 	$('.cate .catearea').hide();

// 	$('.catemom').mouseover(function(){
// 		$('.catearea').slideDown();

// 	});
// 	$('.catemom').mouseleave(function(){
// 		$('.catearea').hide();
// 	});

// 상단 카테고리 슬라이드
$(document).ready(function() {
	$(".catemom").mouseenter(function() {
		var submenu = $(this).next("ul"); // submenu 가 화면상에 보일때는 위로 보드랍게 접고 아니면 아래로 보드랍게 펼치기
		if (submenu.is(":visible")) {
			submenu.slideUp();
		} else {
			submenu.slideDown();
		}
	});
	// .mouseover(function () {
	//   var submenu = $(this)
	//     .next("ul") // submenu 가 화면상에 보일때는 위로 보드랍게 접고 아니면 아래로 보드랍게 펼치기
	//     .slideDown();
	// });
	// .click(function () {
	//   $(this).next("ul").slideDown();
	// })
	// .mosueover(function () {
	//   $(this).slideUp();
	// });

	$("nav li").hover(
		function() {
			$("ul", this).stop().slideDown(200);
		},
		function() {
			$("ul", this).stop().slideUp(200);
		}
	);
});

// 검색어 순위
$(function() {
	const ticker = function() {
		setTimeout(function() {
			$("#ticker li:first").animate({ marginTop: "-20px" }, 200, function() {
				$(this).detach().appendTo("ul#ticker").removeAttr("style");
			});
			ticker();
		}, 4000);
	};
	ticker();
});

// 상단으로 오는 버튼
function clickme() {
	window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
}
// faq
jQuery(function($) {
	$(".faq dd").hide();
	$(".faq dt").click(function() {
		var objNum = $(".faq dd");
		var objIdx = $(".faq dt").index(this);
		for (i = 0; i < objNum.length; i++) {
			if (i == objIdx) {
				$(objNum[objIdx]).slideToggle(100);
			} else if (i != objIdx) {
				$(objNum[i]).slideUp(100);
			}
		}
	});
});

// 오른쪽 네비게이션
// a클릭시 부드럽게 이동
$('a').click(function() {
	$('html, body').animate({
		scrollTop: $($.attr(this, 'href')).offset().top
	}, 500);
	return false;
});

// 퀵메뉴
$('.quick_menu li a').click(function() {
	// 버튼 hover 이벤트
	return false
	$(this).parent().addClass('on');
	$(this).parent().siblings().removeClass('on');
});
// target 위치 표시와, 이동  
var sections = $('.target'),
	nav = $('.quick_menu'),
	nav_height = nav.outerHeight();

$(window).on('scroll', function() {
	var cur_pos = $(this).scrollTop();

	sections.each(function() {
		var top = $(this).offset().top - nav_height,
			bottom = top + $(this).outerHeight();

		if (cur_pos >= top && cur_pos <= bottom) {
			nav.find('a').parent().removeClass('on');
			sections.removeClass('active');

			$(this).parent().addClass('on');
			nav.find('a[href="#' + $(this).attr('id') + '"]').parent().addClass('on');
		}
	});
});

nav.find('a').on('click', function() {
	var $el = $(this),
		id = $el.attr('href');

	$('html, body').animate({
		scrollTop: $(id).offset().top
	}, 500);

	return false;
});


// 원하는 위치에서 스크롤 이벤트
$(window).on('scroll', function() {
	if ($(window).scrollTop() > 520) {
		$('.quick_menu').addClass("fixed");
	} else {
		$('.quick_menu').removeClass("fixed");
	}
})


var searcherrormsg = "검색어를 입력해주세요!!!";
//검색기능 스크립
function searchcheck() {
   if( ! searchform.kw.value ) {
      alert(searcherrormsg);
      return false;
   }
}
