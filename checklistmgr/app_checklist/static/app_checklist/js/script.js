import {getCookie, SendAjax} from "../../../../static/js/modul.js";

let init = () => {      // init
    if (document.getElementById('checklist_man')){      // manager : set the select input on the right value
        let man_id = document.getElementById("id_mgr_id").value;
        if (man_id != 0){
            document.getElementById("man_select").value=man_id;
        }
    }
     if (document.getElementById('checklist_mat')){     // material : set the select input on the right value
        let mat_id = document.getElementById("id_mat_id").value;
        if (mat_id != 0){
            document.getElementById("mat_select").value=mat_id;
        }
    }
     if (document.getElementById('checklist_chklst')) { // checklist : reset the save input (hidden)
         console.log('INIT')
         let chk_save = document.getElementById('id_chk_save').value;
         while (chk_save.length > 0){
         //for (let i=0; i<10; i++){
             let item = chk_save.substring(0, chk_save.indexOf(","));
             chk_save = chk_save.substring(chk_save.indexOf(",") + 1);
             console.log(item)
             let item_id = item.substring(0,item.indexOf(":"));
             if (item_id) {document.getElementById(item_id).checked = true;}

         }

     }
}

window.onload = init();     // init load pages


if (document.getElementById('checklist_man')){      // manager page
    console.log("js man loaded")
    const csrfToken = getCookie('csrftoken');
    document.getElementById("man_select").addEventListener("change", e =>{
        let data = {}
        console.log('click')
        let val = document.getElementById("man_select").value
        console.log(val)
        data['id'] = val;
        if (val == 0) {
            document.getElementById("id_mgr_contact").value = ''
            document.getElementById("id_mgr_phone").value = ''
            document.getElementById("id_mgr_email1").value = ''
            document.getElementById("id_mgr_email2").value = ''
            document.getElementById("id_mgr_id").value = 0
        }
        else {
            // console.log(data)
            data = JSON.stringify(data);
            // ici send ajax
            SendAjax('POST', '/app_checklist/getmanager/', data, csrfToken)
                .done(function (response) {
                    console.log(response)
                    document.getElementById("id_mgr_contact").value = response['mgr_contact']
                    document.getElementById("id_mgr_phone").value = response['mgr_phone']
                    document.getElementById("id_mgr_email1").value = response['mgr_email1']
                    document.getElementById("id_mgr_email2").value = response['mgr_email2']
                    document.getElementById("id_mgr_id").value = val
                })
                .fail(function (response) {
                    console.error("Erreur Ajax : " + response.data);
                    alert("Erreur Ajax - " + response.data);
                });
        }
    })
}

if (document.getElementById('checklist_mat')){      // material page
    console.log("js checklist_mat")
    const csrfToken = getCookie('csrftoken');

    document.getElementById("mat_select").addEventListener("change", e =>{
        let data = {}
        let val = document.getElementById("mat_select").value
        data['id'] = val;
        if (val == 0) {
            document.getElementById("id_mat_registration").value = ''
            document.getElementById("id_mat_type").value = ''
            document.getElementById("id_mat_model").value = ''
            document.getElementById("id_mat_material").value = ''
            document.getElementById("id_mat_manager").value = ''
        }
        else {
            // console.log(data)
            data = JSON.stringify(data);
            // ici send ajax
            SendAjax('POST', '/app_checklist/getmaterial/', data, csrfToken)
                .done(function (response) {
                    console.log(response)
                    document.getElementById("id_mat_registration").value = response['mat_registration']
                    document.getElementById("id_mat_type").value = response['mat_type']
                    document.getElementById("id_mat_model").value = response['mat_model']
                    document.getElementById("id_mat_material").value = response['mat_material']
                    document.getElementById("id_mat_manager").value = response['mat_manager']
                })
                .fail(function (response) {
                    console.error("Erreur Ajax : " + response.data);
                    alert("Erreur Ajax - " + response.data);
                });
        }
    })

}

const save_all = (event) => {
    console.log("save");
    let data_save= []
    const chk_save = document.getElementById('id_chk_save');
    chk_save.value = '';
    let validsElts = document.getElementsByClassName('valid');
    let naElts = document.getElementsByClassName('NA');
    let defaultElts = document.getElementsByClassName('default');
    // valid
    for (let i = 0; i<validsElts.length; i++) {
        if (validsElts[i].firstChild['checked']) {
            let elt = `${validsElts[i].firstChild['id']}:1`
            data_save.push(elt)
        }
    }
    // N/A
    for (let i = 0; i<naElts.length; i++) {
        if (naElts[i].firstChild['checked']) {
            let elt = `${naElts[i].firstChild['id']}:2`
            data_save.push(elt)
        }
    }
    // default
    for (let i = 0; i<defaultElts.length; i++){
        if (defaultElts[i].firstChild['checked']){
            let elt = `${defaultElts[i].firstChild['id']}:3`
            data_save.push(elt)
        }
    }
    data_save.push(',')
    chk_save.value = data_save
    return true
}

if (document.getElementById('checklist_chklst')) {
    console.log("chklist js");
    let form_chk = document.getElementById("form_id");
    form_chk.onsubmit = save_all.bind(form_chk);
}

