export function SendAjax(type='POST' ,url, data, datatype='json', contenttype='application/json' ){
    /*
    Send ajax request to server
    */
    return $.ajax({
        type: type,
        url: url,
        data: data,
        dataType: datatype,
        contentType: contenttype,
    })
};

export function test2(message)
    {
        console.log(message);
    }