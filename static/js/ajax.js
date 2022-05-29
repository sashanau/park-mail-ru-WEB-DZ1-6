$(".vote-up").on('click', function (ev) {
    var $this = $(this)
    $.ajax({
        method: "POST",
        url: "/vote/",
        data: {"id": $this.data('id'), "flag": 1},
        headers: {'X-CSRFToken': csrftoken},
    }).done(function (data) {
        console.log(data.flag)
        if (data.flag == 'bad') {
            alert("Need auth!");
        }
        $(".like-data").text(" Likes: " + data.rating);
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
        $(".like-data").text(" Likes: " + data.rating)
    });
})
$(".ans-data").on('click', function (ev) {
    console.log(1)
    var $this = $(this)
    $.ajax({
        method: "POST",
        url: "/vote-ans/",
        data: {"id_ans": $this.data('id'), "id_ques": $(".vote-down").data('id')},
        headers: {'X-CSRFToken': csrftoken},
    }).done(function (data) {
        if (data.status == 'fail') {
            alert("You are not the author of the question!");
        }
    });
})