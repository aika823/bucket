function like(element, party_id) {
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
                'party_id': party_id,
                'like': like
            },
            method: "POST",
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

// $('.fa-heart').on('click', function() {
//     // like
//     if ($(this).hasClass('far')) {
//         $(this).removeClass('far')
//         $(this).addClass('fas')
//         var like = true
//     }
//     // dislike
//     else {
//         $(this).removeClass('fas')
//         $(this).addClass('far')
//         var like = false
//     }
//     var party_id = $('#partyID').data('party_id')
//     console.log(party_id)
//     $.ajax({
//             url: "/party/like",
//             data: {
//                 'party_id': party_id,
//                 'like': like
//             },
//             method: "POST",
//             success: function(data) {
//                 console.log(data)
//             }
//         })
//         .done(function(json) {
//             console.log("done")
//         })
//         .fail(function(xhr, status) {
//             console.log('fail')
//             console.log(status)
//         })
// });