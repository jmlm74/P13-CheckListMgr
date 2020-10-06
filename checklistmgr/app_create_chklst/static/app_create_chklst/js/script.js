$(function () {
    console.log("Jquery loaded!!!!!")
    console.log(formURL)
    console.log(formURL2)
    $("#create-cat").modalForm({

            // formURL: "http://127.0.0.1:8000/app_create_chklst/createrub/",
            formURL: formURL,
            modalID: "#create-modal"
          });

    $("#create-line").modalForm({

            // formURL: "http://127.0.0.1:8000/app_create_chklst/createrub/",
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
                  {formURL: $(this).data("form-url"),
                  modalID: "#modal"
              });
          });

          // Hide message
          $(".alert").fadeTo(2000, 500).slideUp(500, function () {
              $(".alert").slideUp(500);
          });

})