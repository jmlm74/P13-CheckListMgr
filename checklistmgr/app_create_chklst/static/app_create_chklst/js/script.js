import {SendAjax, getCookie, test2} from '../../../../static/js/modul.js'


/***************************/
/* create/update checklist */
/***************************/
if ((document.getElementById('createchklst'))||(document.getElementById('updatechklst')) ){   // create checklist page
    console.log("JS createchklst-updatechecklst loaded");
    const csrfToken = getCookie('csrftoken');

    // submit the form --> Ajax
    document.getElementById('submit-btn').addEventListener('click', e => {
        let chklst_items = document.getElementById("chklst-items").children;
        let data = {};
        let chk = [];
        let chk_pos = 0;
        const my_array = ['cat', 'lin'];

        const chk_key = document.getElementById('id_chk_key').value;
        const chk_title = document.getElementById('id_chk_title').value;
        const chk_enable = document.getElementById('id_chk_enable').checked;

        if ((chk_key.length === 0) || (chk_title.length === 0) || (chk_enable.length === 0)) {
            alert(inputError);
            return false;
        }

        if (document.getElementById('id_chk_company')) {
            data['chk_company'] = document.getElementById('id_chk_company').value;

        }

        if (document.getElementById('createchklst')){
            data['action'] = 'create'  // create checklist
        }
        else {
            data['action'] = 'update'  // update checklist
        }

        data['chk_key'] = document.getElementById('id_chk_key').value;
        data['chk_title'] = document.getElementById('id_chk_title').value;
        data['chk_enable'] = document.getElementById('id_chk_enable').checked;

        // console.log(`${chk_key} - ${chk_title} - ${chk_enable}`)
        for (let i = 0; i < chklst_items.length; i++) {
            let my_id = chklst_items[i].id.substring(0, 3);
            console.log(my_id)
            if (my_array.includes(my_id)) {
                chk[chk_pos] = chklst_items[i].id;
                chk_pos++;
            }
        }
        data['lines'] = chk;
        // console.log(data)
        data = JSON.stringify(data);
        // ici send ajax
        SendAjax('POST', '/app_create_chklst/create_chklst/', data, csrfToken)
            .done(function () {
                window.location.replace(returnURL)
            })
            .fail(function (response) {
                console.error("Erreur Ajax : " + response.data);
                alert("Erreur Ajax - " + response.data);
            });

    });
}
if (document.querySelector('.dragndrop')) {
/* ***************************** */
/* * Beginning for drag-n-drop * */
/* ***************************** */
    const draggables = document.querySelectorAll('.list-item')
    const containers = document.querySelectorAll('.list')

    draggables.forEach(draggable => {
      draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
      })

      draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging')
      })
    })

    containers.forEach(container => {
      container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')
        if (afterElement == null) {
          container.appendChild(draggable)
        } else {
          container.insertBefore(draggable, afterElement)
        }
      })
    })

    function getDragAfterElement(container, y) {
      const draggableElements = [...container.querySelectorAll('.list-item:not(.dragging)')]

      return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child }
        } else {
          return closest
        }
      }, { offset: Number.NEGATIVE_INFINITY }).element
    }
/* *********************** */
/* * End for drag-n-drop * */
/* *********************** */
}
/* *********************** */
/* * Beginning Modal box * */
/* *********************** */
if ((document.getElementById('catandlinemgmt')) || (document.getElementById('main'))) {    //category and line management page
//JQuery is used for BSModal (Bootstrap)
    $(function () {
        console.log("Jquery loaded!!!!!")
        console.log(formURL)
        console.log(formURL2)
        $("#create-cat").modalForm({
            formURL: formURL,
            modalID: "#create-modal"
        });

        $("#create-line").modalForm({
            formURL: formURL2,
            modalID: "#create-modal"
        });
        var asyncSuccessMessage = [
            "<div ",
            "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
            "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
            "Success: Book was updated.",
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>",
            "<span aria-hidden='true'>&times;</span>",
            "</button>",
            "</div>",
            "<script>",
            "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
            "<\/script>"
        ].join("");

        function updateBookModalForm() {
            $(".update-book").each(function () {
                $(this).modalForm({
                    formURL: $(this).data("form-url"),
                    asyncUpdate: true,
                    asyncSettings: {
                        closeOnSubmit: false,
                        successMessage: asyncSuccessMessage,
                        dataUrl: "books/",
                        dataElementId: "#books-table",
                        dataKey: "table",
                        addModalFormFunction: updateBookModalForm
                    }
                });
            });
        }

        updateBookModalForm();

        // Read and Delete book buttons open modal with id="modal"
        // The formURL is retrieved from the data of the element
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