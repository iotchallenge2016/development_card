
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: {lat: 20.734485, lng: -103.454752},
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    scrollwheel: false,
    draggable: true
  });

  // Define the LatLng coordinates for the polygon's path.
    var zonas = [
          [
            //Entrada
            {lat: 20.733257,lng: -103.454318},
            {lat:20.733214, lng:-103.453773},
            {lat:20.732060, lng:-103.453988},
            {lat:20.732100, lng:-103.454427}

          ],
          [          
            //Oficinas
            {lat:20.734648, lng:-103.454192},
            {lat:20.734598, lng:-103.453548},
            {lat:20.733334, lng:-103.453741},
            {lat:20.733394, lng:-103.454320}
          ],
          [
          //Biblioteca
            {lat:20.734706, lng:-103.453504},
            {lat:20.735208, lng:-103.453461},
            {lat:20.735253, lng:-103.454158},
            {lat:20.734771, lng:-103.454212}
          ],
          [
          //Centro de medios
            {lat:20.735273, lng:-103.453434},
            {lat:20.736041, lng:-103.453300},
            {lat:20.736111, lng:-103.454099},
            {lat:20.735338, lng:-103.454158}
          ],
          [
            //Ingenieria
            {lat:20.737587, lng:-103.453955},
            {lat:20.737442, lng:-103.453081},
            {lat:20.736208, lng:-103.453284},
            {lat:20.736268, lng:-103.454068}
          ],
          [
            //Civil
            {lat:20.736598, lng:-103.452927},
            {lat:20.736482, lng:-103.452249},
            {lat:20.735850, lng:-103.452442},
            {lat:20.735970, lng:-103.453096}
          ],
          [
            //Residencias
            {lat:20.733397, lng:-103.453537},
            {lat:20.733285, lng:-103.452904},
            {lat:20.732653, lng:-103.453065},
            {lat:20.732768, lng:-103.453650}
          ],
          [
            //Centro de congresos
            {lat:20.732395, lng:-103.455972},
            {lat:20.732391, lng:-103.455544},
            {lat:20.732817, lng:-103.454957},
            {lat:20.732784, lng:-103.454568},
            {lat:20.732348, lng:-103.454659},
            {lat:20.732003, lng:-103.455175},
            {lat:20.732071, lng:-103.455811},
            {lat:20.732176, lng:-103.455900}
          ],
          [
            //Visitantes
            {lat:20.732930, lng:-103.457215},
            {lat:20.732895, lng:-103.456461},
            {lat:20.732288, lng:-103.456051},
            {lat:20.731927, lng:-103.456131},
            {lat:20.732118, lng:-103.456917},
            {lat:20.732552, lng:-103.457266}
          ],
          [
            //Medicina
            {lat:20.733987, lng:-103.457808},
            {lat:20.733964, lng:-103.457153},
            {lat:20.732657, lng:-103.457319},
            {lat:20.732697, lng:-103.457892}
          ]
            

        ];

  var i;
  for(i=0; i<zonas.length; i++){
    var zona = new google.maps.Polygon({
      paths: zonas[i],
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35
    });
    zona.setMap(map);
  }
}

function loadCards() {
	$.getJSON('/sections', function(data) {
		var html = "";
		for (var i = data.length - 1; i >= 0; i--) {
			html += "<div class='col s12'>";
			var percentage = Math.round((data[i].max - data[i].capacity) / data[i].max * 100)
			var color = "blue-grey lighten-1";
			if (percentage > 90) {
				color = "red darken-4"
			} else if(percentage > 85) {
				color = "red darken-2"
			} else if(percentage > 70) {
				color = "red"
			} else if(percentage > 60) {
				color = "red lighten-1"
			} else if(percentage > 50) {
				color = "purple darken-1"
			} else if(percentage > 40) {
				color = "blue-grey darken-1"
			}
			html += "<div class='card "+ color +"'>";
			html += "<div class='card-content white-text'>";
			html += "<div class='card-title'>" + data[i].section.replace("P_", "Estacionamiento ") + "</div>";
			html += "<p>Lugares Disponibles: " + (data[i].max - (data[i].max - data[i].capacity)).toString() + "</p>";
			html += "<p>Ocupación: " + percentage + "%</p>"
			html += "</div>"
			html += "</div>"
			html += "</div>";
		}
		console.log('Refreshing')
		$('#cards-container').html(html);
	});
	setTimeout(loadCards, 5000);
}

loadCards();
