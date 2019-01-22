document.getElementById("game_create").addEventListener("click", function () {
    ajax('/game/start/', {}, function () {

    });
});

document.getElementById("game_join").addEventListener("click", function () {
    ajax('/game/join/');
});


function ajax(url, params = {}, result = function (responseText) {
}) {
    $.ajax({
        url: url,
        data: params,
        success: function (response) {
            $('#game_div').html(response);
            result();
        }
    });

}
