function openComment(comment_id) {
    detail_comment = document.getElementById("CommentDetail");
    detail_comment.style.height = "100%";
    detail_comment.style.paddingTop = "60px";
    $.ajax({
            method: "GET",
            url: "/party/get_comment",
            data: {
                comment_id: comment_id,
                name: "John",
                location: "Boston"
            }
        })
        .done(function(result) {
            console.log("대댓글 조회")
            $('#CommentDetail').html(result)
        });
}

function closeComment() {
    document.getElementById("CommentDetail").style.height = "0";
    document.getElementById("CommentDetail").style.paddingTop = "0";
}