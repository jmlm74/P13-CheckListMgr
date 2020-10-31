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
     if (document.getElementById('checklist_chklst')) { // checklist : restore radio buttons and remarks
         // restore radiobuttons states
         let chk_save = document.getElementById('id_chk_save').value;
         while (chk_save.length > 0){
             let item = chk_save.substring(0, chk_save.indexOf(","));
             chk_save = chk_save.substring(chk_save.indexOf(",") + 1);
             let item_id = item.substring(0,item.indexOf(":"));
             if (item_id) {document.getElementById(item_id).checked = true;}
         }
         // restore remarks
         const chk_remsave = document.getElementById('id_chk_remsave').value;
         if(chk_remsave.length>5) {
             let remarks = chk_remsave.split('],[')
             remarks.forEach(remark => {
                 remark = remark.replace('[[', '[');
                 remark = remark.replace(']]', ']');
                 let rem_id = remark.substring(1, remark.indexOf(']['))
                 let rem = remark.substring(remark.indexOf('][')+2, remark.indexOf(']}}'))
                 document.getElementById(rem_id).value = rem
             })
         }
     }
     if (document.getElementById('checklist_fin')) { // checklist_save : the dropzone
     }
}

/* init for the whole pages of the application */
window.onload = init();     // init load pages

/******************************************************/
/* man & mat page --> Ajax the refresh form fields :) */
/******************************************************/
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
/**************************/
/* end of man & mat pages */
/**************************/

/*********************************/
/* Save the checklist - Function */
/*********************************/
const save_all = (event) => {
    // save the radiobuttons state
    let data_save= []
    const chk_save = document.getElementById('id_chk_save');
    chk_save.value = '';
    /***********************************************************/
    /* get all the elements by status the put them in an array */
    /***********************************************************/
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
    // to stop the loop in the init !
    data_save.push(',')
    chk_save.value = data_save
    // save the remarks
    let remark_save = []
    let remarks = document.getElementsByClassName('remarks');
    let chk_remsave = document.getElementById('id_chk_remsave')
    for (let i = 0; i<remarks.length; i++){
        //console.log(remarks[i])
        let remark = `[[${remarks[i].id}][${remarks[i].value}]}}]`
        remark_save.push(remark)
    }
    chk_remsave.value = remark_save
    return true
}
    /******************************************************/
    /* save the check-list on submit (back) or on preview */
    /******************************************************/

if (document.getElementById('checklist_chklst')) {
    console.log("chklist js");
    let form_chk = document.getElementById("form_id");
    form_chk.onsubmit = save_all.bind(form_chk);
}
/********************************************/
/* end of checklist (save and eventhandler) */
/********************************************/

/* *********************** */
/* * Beginning Modal box * */
/* *********************** */
if ((document.getElementById('checklist_mat')) || (document.getElementById('checklist_man'))) {    // manager page
//JQuery is used for BSModal (Bootstrap)
    $(function () {
        console.log("Jquery loaded!!!!!")
        console.log(formURL)
        console.log(formURL2)
        $("#create-mgr").modalForm({
            formURL: formURL,
            modalID: "#create-modal"
        });
        $("#create-mat").modalForm({
            formURL: formURL,
            modalID: "#create-modal"
        });
        $("#create-adr").modalForm({
            formURL: formURL,
            modalID: "#create-modal-large"
        });
        $("#create-line").modalForm({
            formURL: formURL2,
            modalID: "#create-modal"
        });

        $(".bs-modal-large").each(function () {
            $(this).modalForm(
                {
                    formURL: $(this).data("form-url"),
                    modalID: "#modal-large"
                });
        });

        $(".bs-modal").each(function () {
            $(this).modalForm(
                {
                    formURL: $(this).data("form-url"),
                    modalID: "#modal"
                });
        });

        // Hide message
        $(".alert").fadeTo(2000, 500).slideUp(500, function () {
            $(".alert").slideUp(500);
        });

    });
}
/* ********************* */
/* * Beginning end box * */
/* ********************* */


if (document.getElementById('checklist_fin')) { // checklist_save : the dropzone

    /************/
    /* DROPZONE */
    /************/
    Dropzone.autoDiscover = false;
    let caption = "";
    // console.log(uploadURL)
    $(function()
    {
         var myDropzone = new Dropzone("div#dropzoneForm", {
            url: uploadURL,
            maxFiles: 5,
            maxFilesize: 5,
            acceptedFiles: '.png, .jpg, .jpeg',
            addRemoveLinks: true,
            params: {newchecklist_id: newchecklistID}
        });

        let fotos = document.getElementById("id_cld_fotosave").value;
        if (fotos.length >5) {
            // console.log(fotos)
            fotos = fotos.replace('[', '')
            fotos = fotos.replace(']', '')
            fotos = fotos.replace(/\'/g, '')
            fotos = fotos.split(', ')  // now fotos is an array
            // console.log(fotos)

            fotos.forEach(foto => {
                // console.log(foto)
                let filename = foto.split('\\').pop().split('/').pop();
                // let x = foto.replace(/\..+$/, '');
                var mockFile = {name: filename, status: Dropzone.ADDED, accepted: true};
                let thumbnail = "/media/" + foto
                // console.log(thumbnail)
                myDropzone.displayExistingFile(mockFile, thumbnail);
            });
        }
        myDropzone.on("addedfile", e => {
            caption = prompt(promptmsg);
        });
        myDropzone.on("sending", function(file, xhr, formData){
           formData.append('caption', caption)
        });
        myDropzone.on("removedfile", file => {
            let data={}
            const csrfToken = getCookie('csrftoken');
            data['filename'] = file.name
            data['checklist_id'] = newchecklistID
            data = JSON.stringify(data);
            // ici send ajax
            SendAjax('POST', removeURL, data, csrfToken)
            .done(function (response) {
                console.log(response)
            });
        });
    });
    /****************/
    /* FIN DROPZONE */
    /****************/
    const csrfToken = getCookie('csrftoken');
    document.getElementById("pdf-preview").addEventListener("click", e => {
        let data = {}
        data['cld_key'] = document.getElementById("id_cld_key").value
        data['cld_valid'] = document.getElementById("id_cld_valid").checked
        data['cld_remarks'] = document.getElementById("id_cld_remarks").value
        data = JSON.stringify(data);
            // ici send ajax
            SendAjax('POST', '/app_checklist/beforepreview/', data, csrfToken)
                .done(function (response) {
                    return true;
                });
    });
}