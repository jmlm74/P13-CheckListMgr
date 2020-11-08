export function SendAjax(type='POST' ,
                         url,
                         data,
                         csrftoken = "",
                         datatype='json',
                         contenttype='application/json'){
    /*
    Send ajax request to server
    */
    return $.ajax({
        type: type,
        url: url,
        data: data,
        dataType: datatype,
        contentType: contenttype,
        headers: {'X-CSRFToken': csrftoken }
    })
};

export function test2(message)
    {
        console.log(message);
    }

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
