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

    if (document.querySelector("#company-create-form")){  // Create company page
        let address_elt = document.querySelector('#id_address');
        address_elt.addEventListener('change', item => {
            // console.log("Change");
            if (!address_elt.value){
                document.getElementById('id_address_name').value = '';
                document.getElementById('id_street_number').value = '';
                document.getElementById('id_street_type').value = '';
                document.getElementById('id_address1').value = '';
                document.getElementById('id_address2').value = '';
                document.getElementById('id_city').value = '';
                document.getElementById('id_zipcode').value = '';
                document.getElementById('id_country').value = '';
                return
            }
            // console.log(address_elt.value);
            let data = {};
            data['id'] = address_elt.value;
            data = JSON.stringify(data);
            SendAjax('POST','/app_utilities/get_address/',data)
            .done(function(response){
            // console.log(response.address);
                let addr=JSON.parse(response.address)[0];  //just to get the 1st elem
                // console.log(addr);
                console.log(addr['fields']);
                document.getElementById('id_address_name').value = addr['fields']['address_name'];
                document.getElementById('id_street_number').value = addr['fields']['street_number'];
                document.getElementById('id_street_type').value = addr['fields']['street_type'];
                document.getElementById('id_address1').value = addr['fields']['address1'];
                document.getElementById('id_address2').value = addr['fields']['address2'];
                document.getElementById('id_city').value = addr['fields']['city'];
                document.getElementById('id_zipcode').value = addr['fields']['zipcode'];
                document.getElementById('id_country').value = addr['fields']['country'];
            })
            .fail( function(response) {
                console.error("Erreur Ajax : " + response.data);
                alert("Erreur Ajax - "+ response.data);
            });

        })
    }
}
if (document.querySelector("#list_users")) {    // list users page
    console.log("In list users page")
    let data_msg={}
    data_msg['msg'] = 'Userdeletequestion'
    data_msg = JSON.stringify(data_msg)
    var msg_delete = ""
    // just to get the delete msg
    SendAjax('POST', '/app_utilities/get_message/',data_msg)
    .done(function(response){
        msg_delete = response['msg']
    })
    // if click on trash --> get the id
     document.querySelectorAll('.trash').forEach(item => {
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
               // console.log("don't delete")
            }
        });
    });
}
