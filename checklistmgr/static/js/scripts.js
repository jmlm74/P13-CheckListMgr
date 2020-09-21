"use strict";
console.log("corejs loaded !");

let legal_click_elt = document.getElementById("legal-click");
let legal_text = document.getElementById('lega')
let contrib_click_elt = document.getElementById("contrib-click");
let contrib_text = document.getElementById('contrib')
let display_text = document.getElementById("affiche")


legal_click_elt.onclick = function(){
    display_text.innerHTML=legal_text.innerHTML;
    let textElt = document.querySelector("textarea.legal")
    textElt.setSelectionRange(0,0)
}

contrib_click_elt.onclick = function(){
    display_text.innerHTML=contrib_text.innerHTML;
}

