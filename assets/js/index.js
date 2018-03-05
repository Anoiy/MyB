$(document).ready(function (e) {
    var page = $('#cur_page').val();
    $('.ul_par li').each(function () {
       if($(this).text() == page) {
           $(this).removeClass('par_un');
           $(this).addClass('par_active')
       }
    });

    var flag = "left";
    var point = -1200;
    var set;
    function showImage () {
        if (point == -4800) {
            flag = "right";
        } else if (point == 0) {
            flag = "left";
        }
        if (flag == "left") {
            $(".imgs").animate({left:point}, 1000);
            point -= 1200;
        }else if (flag == "right") {
            $(".imgs").animate({left:0}, 1500);
            point = 0;
        }
    }
    set=setInterval(showImage, 3000);
    // each（）方法是遍历li对象数组，里面的index就是这个数组中对应的下标
    $(".img_index li").each(function (index, element) {
        $(this).mouseover(function (e) {
            point = -1200 * index;
            $(".imgs").animate({left: point}, 300);
        });
    });
});

$(function () {
    $('.ul_par li').on('click', function () {
        var choose_page = $(this).text();
        var cur = $('#cur_page');
        var cur_page = cur.val();
        var page_nums = $('#page_num').val();

        if (choose_page == '上一页') {
            if(cur_page == '1') {
                return 0;
            } else {
                cur_page = parseInt(cur_page) - 1;
                cur.val(cur_page);
            }
        } else if (choose_page == '下一页') {
            if(cur_page == page_nums) {
                return 0;
            } else {
                cur_page = parseInt(cur_page)  + 1;
                cur.val(cur_page);
            }
        } else {
            cur_page = choose_page;
            cur.val(cur_page);
        }
        window.location.href = '/?page=' + cur_page;
        // try {
        //     page = parseInt(page);
        //     $('#cur_page').val(page);
        //     var request_url = '/?page=' + page;
        //     window.location.href = request_url
        // } catch (e){
        //     var cur_page = $('#cur_page').val();
        //     var page_num = $('#page_num').val();
        //     if (cur_page == 1 && $(this).text() == '上一页') {
        //         return 0;
        //     } else if (cur_page == page_num && $(this).text() == '下一页') {
        //         return 0;
        //     } else if ($(this).text() == '上一页'){
        //         page = parseInt(cur_page) - 1;
        //         $('#cur_page').val(page);
        //     } else if ($(this).text() == '下一页'){
        //         page = parseInt(cur_page) + 1;
        //         $('#cur_page').val(page);
        //     }
        //     var request_url = '/?page=' + page;
        //     window.location.href = request_url;
        // }
    });
});










