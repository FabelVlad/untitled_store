/* Project specific Javascript goes here. */

$(document).ready(function () {
    const $myLikeForm = $('#like-form')
    $myLikeForm.submit(function (event) {
        event.preventDefault()
        const $formData = $(this).serialize()
        const $thisURL = $myLikeForm.attr('action')
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: function (data) {
                $("#likes-count").html(data['likes']);
            },
        })
    })

    const $myCartForm = $('#cart-form')
    $myCartForm.submit(function (event) {
        event.preventDefault()
        const $formData = $(this).serialize()
        const $thisURL = $myCartForm.attr('action')
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: function (data) {
                $("#items_in_cart").html(data['items_in_cart']);
                $myCartForm[0].reset();
                const messages = data['messages']
                $.each(messages, function () {
                    let item = $('<div class="alert alert-' + $(this).attr('tags') + '">' + $(this).attr('message') + '</div>');
                    item.appendTo($('#messages')).delay(3000).slideUp(200, function () {
                        item.remove();
                    });
                });
            },
            error: function (data) {
                console.log('error')
            }
        })
    })
})