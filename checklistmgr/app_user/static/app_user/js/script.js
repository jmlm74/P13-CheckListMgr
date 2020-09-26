import {SendAjax, test2} from '../../../../static/js/modul.js '
console.log('js app_user loaded !')
// wait for the dom complete load
window.onload = function () {
    if (document.querySelector("#id_confirm_password")) {  // create_user page
        // valid password and confirm password length
        const password_confirm = document.querySelector("#id_confirm_password");
        const password = document.querySelector("#id_password");

        password_confirm.addEventListener('blur', event => {
            if ((event.target.value.length < 8) || (password.value.length < 8)) {
                alert("password & confirmation : 8 chars min !")
                password.focus();
            }
        });
    }

    if (document.querySelector("#list_users")) {    // list users page
        let data_msg={}
        data_msg['msg'] = 'Userdeletequestion'
        data_msg = JSON.stringify(data_msg)
        var msg_delete = ""
        SendAjax('POST', '/app_utilities/get_message/',data_msg)
        .done(function(response){
            msg_delete = response['msg']
            console.log(msg_delete)
        })

         document.querySelectorAll('.fa-trash-alt').forEach(item => {
            item.addEventListener('click',event => {
                console.log(item.id);
                let pos = item.id.indexOf('-');
                let id = item.id.substr(0,pos);
                let username = item.id.substr(pos+1);
                if (window.confirm(`${msg_delete} : ${username} ?`)){
                    let data={}
                    data['id'] = id
                    data = JSON.stringify(data);
                    SendAjax('POST','/app_user/delete_user/',data)
                    .done(function(response){
                        let elt_to_remove = document.getElementById(id)
                        elt_to_remove.parentNode.removeChild(elt_to_remove)
                    })
                    .fail( function(response) {
                        console.error("Erreur Ajax : " + response.data);
                        alert("Erreur Ajax - "+ response.data);
                    });
                }
                else {
                    console.log("don't delete")
                }
            });
        });
    }
}

