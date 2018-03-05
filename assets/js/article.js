// $(function () {
//     $('#com_sub').submit(function () {
//         var content = $('#comment_cont').val();
//         $(this).ajax({
//             type: 'post',
//             dataType: 'text',
//             url: "{% url 'article' %}",
//             data: {'content': content},
//             success: function (data) {
//                 LoadNewComment();
//                 $('#comment_cont').val("");
//             }
//         });
//         return false;
//     })
// });
//
// function LoadNewComment() {
//     var article_id = $('#article_id').val();
//     $(this).ajax({
//         type: 'post',
//         dataType: 'text',
//         url: "{% url 'comment' %}",
//         data: {'article_id': article_id},
//         success: function (data) {
//             if(data.length > 0) {
//                 $('#')
//             }
//         }
//     })
// }

$(function () {
    $('#com_sub').on('click', function () {
        var comment_content = $('#comment_cont').text();
        var article_id = $('#article_id').val();
        if(comment_content == "") {
           alert('评论不能为空');
            return 0;
        }
        $.ajax({
            cache: false,
            type: 'POST',
            data: {'article_id': article_id, 'comment_content': comment_content},
            async: true,
            url: "/comment/",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function (data) {
                window.location.reload()
            }
        })
    });
});

























