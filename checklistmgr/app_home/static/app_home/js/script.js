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







