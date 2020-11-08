import {SendAjax, getCookie, test2} from '../../../../static/js/modul.js'
console.log("app_home js loaded !!")

var lat, lon;

/************************************
 * GeoLoc --> map display + weather *
 ************************************/
if (document.getElementById('map')){   // map exists --> on the homepage
    window.onload = function () {
        function geoloc(callback) {
            navigator.geolocation.getCurrentPosition(function (position) {
                lat = position.coords.latitude;
                lon = position.coords.longitude;
                let mymap = L.map('map').setView([lat, lon], 11);
                let marker = L.marker([lat, lon]).addTo(mymap);
                // get the tiles
                L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
                    // not a copyright but logical !
                    attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
                    minZoom: 1,
                    maxZoom: 20
                }).addTo(mymap);

                if (typeof callback == "function")
                    callback();
            });
        }

        geoloc(function () {
            var fetch_url_current = 'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon +
                '&appid=7093f6d8c4e0b521741e195b40b1347d&lang=fr&units=metric';
            fetch(fetch_url_current)
                .then(res => res.json())
                .then(resJson => DisplayWeather(resJson));
        });

    }

    function DisplayWeather(resJson) {
        // console.log(resJson);
        let my_div = document.querySelector("#weather");
        let title = document.createElement('h3');
        title.appendChild(document.createTextNode("Météo à " + resJson.name));
        my_div.appendChild(title);
        let ligne = document.createElement('h4');
        ligne.appendChild(document.createTextNode(resJson.main.temp + "°C"));
        my_div.appendChild(ligne);
        let img = document.createElement('img');
        // console.log("https://openweathermap.org/img/wn/" + resJson.weather[0].icon + ".png");
        img.src = "https://openweathermap.org/img/wn/" + resJson.weather[0].icon + ".png";
        my_div.appendChild(img);
        ligne = document.createElement("p");
        ligne.classList.add("small");
        ligne.appendChild(document.createTextNode(resJson.weather[0].description));
        my_div.appendChild(ligne);
        ligne = document.createElement('hr');
        my_div.appendChild(ligne);


        // call the forecast
        var fetch_url_forecast = 'https://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + lon +
            '&appid=7093f6d8c4e0b521741e195b40b1347d&lang=fr&units=metric';
        fetch(fetch_url_forecast)
            .then(result => result.json())
            .then(resJsonForecast => DisplayForecastWeather(resJsonForecast));
    }

    function DisplayForecastWeather(resJson) {
        // console.log("Dans displayForecastWeather");

        let my_div = document.querySelector("#weather");
        let new_div = document.createElement('div');
        new_div.classList.add("row");
        new_div.classList.add("col-12");
        new_div.classList.add("forecast");
        my_div.appendChild(new_div);
        for (var i = 1; i < 7; i++) {
            let new_div = document.querySelector(".forecast");
            let heure = (resJson.list[i].dt_txt).substr(11, 5);
            let desc = resJson.list[i].weather[0].description;
            let icon = resJson.list[i].weather[0].icon;
            // console.log(heure + "-" + desc + "-" + icon);
            let new_littlediv = document.createElement('div');;
            new_littlediv.classList.add("col-2");
            new_littlediv.classList.add("small");
            new_littlediv.classList.add("justify-center");
            new_littlediv.classList.add("forecast-" + i);
            // new_littlediv.classList.add("toto")

            new_div.appendChild(new_littlediv);
            let ligne1 = document.createElement('p');
            ligne1.appendChild(document.createTextNode(heure));
            new_littlediv.appendChild(ligne1);
            let img = document.createElement('img');
            img.src = "https://openweathermap.org/img/wn/" + icon + ".png";
            img.classList.add("center-block");
            new_littlediv.appendChild(img);
            document.createElement('p').appendChild(document.createTextNode(desc));
            new_littlediv.appendChild(ligne1);

        }
    }
}
/************************************/
/* End of geoloc and weather report */
/************************************/

/*************************************************/
/* the trick for the legal page                  */
/* hide or display the legal or the contrib page */
/*************************************************/

if (document.querySelector("#lega")){  // legal page
    let legal_click_elt = document.getElementById("legal-click");
    let legal_text = document.getElementById('lega')
    let contrib_click_elt = document.getElementById("contrib-click");
    let contrib_text = document.getElementById('contrib')
    let display_text = document.getElementById("affiche")

    contrib_click_elt.onclick = function () {
        display_text.innerHTML = contrib_text.innerHTML;
    }

    legal_click_elt.onclick = function () {
        display_text.innerHTML = legal_text.innerHTML;
        let textElt = document.querySelector("textarea.legal")
        textElt.setSelectionRange(0, 0)
    }
}

if (document.querySelector("#form-search")) {
    const csrfToken = getCookie('csrftoken');
    const search_mat = document.getElementById('search-material');
    const search_man = document.getElementById('search-manager');
    const search_date = document.getElementById('search-date');
    const search_btn = document.getElementById('search-button');

    const get_materials = (manager) =>{
        let data={}
        let l = search_mat.options.length - 1;
        for (let i=l; i>=0; i--){
            search_mat.remove(i);
        }
        if (manager){
               data['manager'] = manager;
        } else {
            data['manager'] = '';
        }
        data = JSON.stringify(data);
        SendAjax('POST', '/app_home/autocomplete_search_mat/', data, csrfToken)
            .done(function (response) {

                // if(!manager) {
                    let newOption = document.createElement("option");
                    newOption.text = '-------';
                    newOption.value = 0;
                    search_mat.appendChild(newOption);
                // }
                response.forEach(element =>{
                    let newOption = document.createElement("option");
                    newOption.text = element['fields']['mat_designation'];
                    newOption.value = element['pk'];
                    search_mat.appendChild(newOption);
                    })

            })
            .fail(function (response) {
                console.error("Erreur Ajax : " + response.data);
            });
    }

    const get_managers = (material) => {
        let data={};
        let l = search_man.options.length - 1;
        for (let i=l; i>=0; i--){
            search_man.remove(i);
        }
        if (material){
               data['material'] = material;
        } else {
            data['material'] = '';
        }
        data = JSON.stringify(data);
        SendAjax('POST', '/app_home/autocomplete_search_man/', data, csrfToken)
        .done(function (response) {
            if(!material) {
                let newOption = document.createElement("option");
                newOption.text = '-------';
                newOption.value = 0;
                search_man.appendChild(newOption);
            }
            response.forEach(element =>{
                let newOption = document.createElement("option");
                newOption.text = element['fields']['mgr_name'];
                newOption.value = element['pk'];
                search_man.appendChild(newOption);
                })
        })
        .fail(function (response) {
            console.error("Erreur Ajax : " + response.data);
        });
    }

    const get_checklists = () => {
        let data = {};
        if (search_man.value != '0'){
            data['manager'] = search_man.value
        }
        if (search_mat.value != '0'){
            data['material'] = search_mat.value
        }
        if (search_date.value != ''){
            data['date'] = search_date.value
        }
        let ul_ckklsts = document.getElementById('ul-chklsts')
        ul_ckklsts.innerHTML='';

        data = JSON.stringify(data);
        SendAjax('POST', '/app_home/search_chklst/', data, csrfToken)
        .done(function (response) {
            console.log(response);
            response.forEach(element =>{
                console.log(element);
                let a = document.createElement('a')
                let li = document.createElement('li')
                li.id=element.key
                let color_text = "text-success";
                if (!element.valid){color_text = "text-danger"}
                li.className="mt-1"
                li.classList.add(color_text)
                let html_1 ="";
                if ('company' in element){html_1 = `${html_1}${element.company} - `}
                if (element.manager != "") {html_1 = `${html_1}${element.manager} - `}
                if (element.material != "") {html_1 = `${html_1}${element.material} - `}
                html_1 = `${html_1}${element.key} - ${element.date} - ${element.title}`
                li.appendChild(document.createTextNode(html_1));
                a.setAttribute("href",element.pdf);
                a.setAttribute('target',"_blank");
                ul_ckklsts.appendChild(a);
                a.appendChild(li);
            })
        })
        .fail(function (response) {
            console.error("Erreur Ajax : " + response.data);
        });


    }

    const init = () => {
        get_materials();
        get_managers();
        search_date.value='';
    }
    // form main page
    window.onload = init();

    search_mat.addEventListener('change', e => {
        if (search_man.value === '0') {
            get_managers(search_mat.value);
        }
    })
    search_man.addEventListener('change', e =>{
        if (search_mat.value === '0') {
            console.log(search_man.value)
            get_materials(search_man.value);
        }
    })
    search_btn.addEventListener('click', e =>{
        get_checklists();
        init();
        e.preventDefault()
    })
}








