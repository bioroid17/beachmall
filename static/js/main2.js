$(document).ready(function () {

    // scrollbar event
    $("body").niceScroll({
        // 스크롤바 너비
        cursorwidth: "0.8vw",
        // 스크롤바 외곽선
        cursorborder: false,
        // 스크롤 속도
        scrollspeed: 20,
        // 스크롤 최소 높이
        cursorminheight: 30,
        // 스페이스바 활성
        spacebarenabled: false,
        cursorfixedheight: 50,
    });

    // background animation
    $(document).on("mousewheel scroll touchmove", function () {
        $("#container").addClass("animation_on");
    })

    // fixbackground event
    const scroll_body = $("#wrap"); // 스크롤 부모
    const fix_bg = $(".fix_background"); // 고정 배경
    let scroll_ps = $(".scroll_position"); // 스크롤 위치

    let scroll_height; // 스크롤 높이 
    let scroll_Real_Height; // 실제 스크롤 높이값
    let scroll_Top; // 스크롤바 높이
    let scroll_percent; // 스크롤값 백분율
    let distance; // 요소가 움직일 거리

    function seting() {

        let window_height = $(window).height(); // 윈도우 높이

        scroll_height = scroll_body.height(); // 스크롤 높이

        scroll_Real_Height = scroll_height - window_height; // 실제로 스크롤 높이값

        scroll_Top = $(window).scrollTop(); // 스크롤바의 현재 위치

        let window_percent = scroll_Top / scroll_Real_Height; // 거리와 현재 위치를 기준으로 비율

        scroll_percent = window_percent * 100;
        // 백분율

        distance = window_percent * 1; // 스크롤 움직일값

        distance = parseFloat(distance);
        // console.log(distance);
    }

    function fix_background_event() {

        let op = fix_bg.css("opacity");

        // 스크롤 비율에 따른 고정배경 값

        if (distance >= 0 && distance <= 0.5) {
            fix_bg.css({
                opacity: 0.3 + distance,
            });
        } else if (distance >= 0.5) {
            fix_bg.css({
                opacity: 1.3 - distance,
            });
        }

        // console.log(op);

    }

    function event_scroll() {
        seting();
        fix_background_event();
    }

    // 스크롤바 이벤트 최초실행
    function play() {
        event_scroll();
    }

    // 스크롤 이벤트 바인딩
    $(window).scroll(function (e) {
        event_scroll();
        section_3_item();
        scroll_direction_event();
    });

    // section 3 item event 함수
    function section_3_item() {
        let trigger; // 스크롤 이벤트 발생위치

        trigger = $(".l_item_1").offset().top; // item 위치값

        if (scroll_Top + 450 >= trigger) {
            $(".l_item_1").addClass("event");
            $(".l_item_2").addClass("event_2");
            $(".l_item_3").addClass("event_3");
        }
    }



    // 스크롤 방향에 따른 메뉴바 이벤트

    var lastScrollTop = 0; // 마지막 스크롤 높이

    function scroll_direction_event() {

        var st = $(this).scrollTop(); // 현재 높이 측정

        if (st > lastScrollTop) { // 현재 높이가 마지막 높이값 보다 크다면

            console.log("down");
            $("#header").addClass("scroll_on");

        } else if (st == lastScrollTop) {

        } else {

            console.log("up");
            $("#header").removeClass("scroll_on");

        }

        lastScrollTop = st; // 마지막 높이값 초기화
    }





    // 메뉴 애니메이션
    $(".hamburger").click(function () {
        $(this).toggleClass("is-active");
    });

    // GNB 애니메이션

    let menu_on_off = true;

    $(".hamburger").click(function () {
        if (menu_on_off) {
            $("#header").addClass("menu_on");
            menu_on_off = false;
        } else {
            $("#header").removeClass("menu_on");
            menu_on_off = true;
        }
    });

    // 타이핑 애니메이션
    var typingBool = false;
    var typingIdx = 0;
    var liIndex = 0;
    var liLength = $(".typing-txt > ul > li").length;
    var del = -1;
    var repeatInt = false;
    // 타이핑될 텍스트를 가져온다 
    var typingTxt = $(".typing-txt > ul > li").eq(liIndex).text();
    //liIndex 인덱스로 구분해 한줄씩 가져옴

    typingTxt = typingTxt.split(""); // 한글자씩 잘라 배열로만든다

    if (typingBool == false) { // 타이핑이 진행되지 않았다면 
        typingBool = true;
        var tyInt = setInterval(typing, 100); // 반복동작 
    }

    function typing() {
        $(".typing ul li").removeClass("on");
        $(".typing ul li").eq(liIndex).addClass("on");
        //현재 타이핑되는 문장에만 커서 애니메이션을 넣어준다.

        if (typingIdx < typingTxt.length) { // 타이핑될 텍스트 길이만큼 반복 
            $(".typing ul li").eq(liIndex).append(typingTxt[typingIdx]); // 한글자씩 이어준다. 
            typingIdx++;
        } else { //한문장이끝나면
            if (liIndex < liLength - 1) {
                //다음문장으로  가기위해 인덱스를 1증가
                liIndex++;
                //다음문장을 타이핑하기위한 셋팅
                typingIdx = 0;
                typingBool = false;
                typingTxt = $(".typing-txt>ul>li").eq(liIndex).text();

                //다음문장 타이핑전 1초 쉰다
                clearInterval(tyInt);
                //타이핑종료

                setTimeout(function () {
                    //1초후에 다시 타이핑 반복 시작
                    tyInt = setInterval(typing, 100);
                }, 300);
            } else if (liIndex == liLength - 1) {

                //마지막 문장까지 써지면 반복종료
                clearInterval(tyInt);
            }
        }
    }
})