// https://docs.djangoproject.com/en/1.8/ref/csrf/#ajax
// using jQuery
//
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).on("ajaxSend", function (event, xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !settings.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
    }
})
