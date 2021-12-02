function like(element, id, table = 'party') {
    //like
    if ($(element).hasClass('far')) {
        $(element).removeClass('far')
        $(element).addClass('fas')
        count = $(element).siblings('p')
        count.text(Number(count.text()) + 1)
        var like = true
    }
    //unlike
    else {
        $(element).removeClass('fas')
        $(element).addClass('far')
        count = $(element).siblings('p')
        count.text(Number(count.text()) - 1)
        var like = false
    }
    $.ajax({
            url: "/party/like",
            data: {
                'table': table,
                'id': id,
                'like': like
            },
            method: "GET",
            success: function(data) {
                console.log(data)
            }
        })
        .done(function(json) {
            console.log("done")
        })
        .fail(function(xhr, status) {
            console.log('fail')
            console.log(status)
        })
}