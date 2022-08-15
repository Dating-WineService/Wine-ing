$(function(){
    /* Slick Slider - Welcome */
    $('.slideshow').slick({
	    infinite: true, // 무한반복
	    dots: false, // 동그라미 네비게이션 사용안함
	    autoplay: true, // 자동 재생
	    autoplaySpeed: 2000, // 자동 재생 시 머무는 시간
	    fade: true, // 크로스 페이드 트랜지션
	    speed: 1000, // 자동 재생 트랜지션 시간
	    pauseOnHover: false // 마우스 오버될 때 멈춤 사용안함
    });

    /* TypeIt - Welcome */
    $('#typing').typeIt({
	    strings: ["와인서비스"], // 타이핑 텍스트 입력
	    speed: 100, // 알파벳 타이핑 속도
	    autoStart: true, // 자동 재생 사용
	    breakLines: false, // 줄 바꿈 사용안함
    });

})