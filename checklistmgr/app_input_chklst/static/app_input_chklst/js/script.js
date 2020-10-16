/* *********************** */
/* * Beginning Modal box * */
/* *********************** */
if ((document.getElementById('mgrmgmt')) || (document.getElementById('main'))) {    // manager page
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