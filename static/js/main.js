var polygons = [];

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: {lat: 20.734485, lng: -103.454752},
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    scrollwheel: true,
    draggable: true
  });

  var zones = [];
  var percentages = [];
  $.getJSON('/sections', function(data) {
  	for (var i = data.length - 1; i >= 0; i--) {
  		zones.push(data[i].location);
  		percentages.push(Math.floor((data[i].max - data[i].capacity) / data[i].max * 100));
  	}
    for (var i = zones.length - 1; i >= 0; i--) {
      var zone = new google.maps.Polygon({
        paths: zones[i],
        strokeColor: getColorClass(percentages[i])[1],
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: getColorClass(percentages[i])[1],
        fillOpacity: 0.35
      });
      polygons.push(zone);
      zone.setMap(map);
    }  	
  })

}


function getColorClass(percentage) {
	
	if (percentage > 90) {
		return ["red accent-4", "#d50000"];
	} else if(percentage > 80) {
		return ["red", "#f44336"];
	} else if(percentage > 70) {
		return ["orange", "#ff9800"];
	} else if(percentage > 60) {
		return ["amber darken-3", "#ff8f00"];
	} else if(percentage > 40) {
		return ["yellow accent-2", "#ffff00"];
	} else if(percentage > 20) {
		return ["lime accent-4", "#aeea00"];
	} else {
		return ["light-green accent-3", "#76ff03"];
	}
}

function loadCards() {
  $.getJSON('/sections', function(data) {
    var html = "";
    for (var i = data.length - 1; i >= 0; i--) {
      html += "<div class='col s12'>";
      var percentage = Math.floor((data[i].max - data[i].capacity) / data[i].max * 100);
    	html += "<div class='card "+ getColorClass(percentage)[0] +"'>";
    	html += "<div class='card-content white-text'>";
    	html += "<div class='card-title'>" + data[i].section.replace("P_", "Estacionamiento ") + "</div>";
    	html += "<p>Lugares Disponibles: " + (data[i].max - (data[i].max - data[i].capacity)).toString() + "</p>";
    	html += "<p>Ocupación: " + percentage + "%</p>";
    	html += "</div>";
    	html += "</div>";
    	html += "</div>";
      if (polygons.length > 0) {
        polygons[i].setOptions({
          strokeColor: getColorClass(percentage)[1],
          fillColor: getColorClass(percentage)[1]
        });
      }
		}
		console.log('Refreshing')
		$('#cards-container').html(html);
	});
	setTimeout(loadCards, 2000);
}



loadCards();
