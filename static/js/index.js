$(".vote-up").on('click', function (ev) {
    var $this = $(this)
    $.ajax({
        method: "POST",
        url: "/vote/",
        data: {"id": $this.data('id'), "flag": 1},
        headers: {'X-CSRFToken': csrftoken},
    }).done(function (data) {
        console.log(data.rating)
        console.log($this.data('id'))
        $(".like-data" + $this.data('id')).text(" Likes: " + data.rating)
    });
})
$(".vote-down").on('click', function (ev) {
    var $this = $(this)
    $.ajax({
        method: "POST",
        url: "/vote/",
        data: {"id": $this.data('id'), "flag": 0},
        headers: {'X-CSRFToken': csrftoken},
    }).done(function (data) {
        console.log(data.rating)
        console.log($this.data('id'))
        $(".like-data" + $this.data('id')).text(" Likes: " + data.rating)
    });
})