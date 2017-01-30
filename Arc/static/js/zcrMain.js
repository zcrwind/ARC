//zcr写的js代码

$(function()
{
	'use strict';

	var sidebar = $('#overlay-sidebar');
	var overlay = $('#overlay');
	var sidebar_trigger = $('#sidebar_trigger');//侧栏触发器（MENU链接）
	var backButton = $('#back-to-top');

	// console.log(sidebar_trigger);
	function showSidebar()
	{
		// console.log('clicked!');
		overlay.fadeIn();
		sidebar.animate({'right':0},450);//450ms是动画的速度（越小动画越快，猜测是动画的执行时间）
	}
	function hideSidebar()
	{
		overlay.fadeOut();
		sidebar.animate({'right':-sidebar.width()});
	}
	sidebar_trigger.on('click',showSidebar);
	overlay.on('click',hideSidebar);

	backButton.on('click',function()
	{
		// console.log('back!');
		/*下面的返回顶部动画貌似是由慢到快，怎么让它由快到慢呢？*/
		$('html,body').animate({
			scrollTop: 0
		}, 700)
	})

	$(window).on('scroll',function()
	{
		if($(window).scrollTop() > $(window).height())
		{
			backButton.fadeIn();//显示
		}
		else
		{
			backButton.fadeOut();//隐藏
		}
	})
	/*让程序自动触发scroll事件，达到防治页面一刷新或者首次加载时出现“返回顶部”按钮。但是有问题：首次
	 *加载页面或者是刷新时，“返回顶部”按钮会闪一下...
	 */
	$(window).trigger('scroll');

})
