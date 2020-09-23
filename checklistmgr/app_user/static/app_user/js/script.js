console.log('js app_user loaded !')

const password_confirm = document.querySelector("#id_confirm_password");
const password = document.querySelector("#id_password");

password_confirm.addEventListener('blur', event => {
    if ((event.target.value.length <8) || (password.value.length <8)) {
        alert("password & confirmation : 8 chars min !")
        password.focus();
    }
});