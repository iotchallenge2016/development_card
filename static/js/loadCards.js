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