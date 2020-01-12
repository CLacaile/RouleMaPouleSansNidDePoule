var vectorSource;

var vectorLayer;
var mapBackground;
var mapView;
var map;
var arrayMarker = new Array();

var urlLogin = 'http://localhost:8000/api/token/';

var urlWaypoint = 'http://localhost:8000/api/v1.0/output/roadgrade/';

$('#Modal-login').modal({
	keyboard: false,
	backdrop: 'static',
	hide : false
});



$('#loginForm').submit(function(e){
	e.preventDefault();
	$.ajax({
		url: urlLogin,

		method:'POST',
		data:$('#loginForm').serialize(),
		success : function(data, textStatus, jqXHR ){

			$('#Modal-login').modal('hide');
			document.cookie= data.access;
			loadWaypoints();
		},

		error : function(jqXHR, statut, erreur){

		}
	});
});


function loadWaypoints() {
	$.ajax({
		url: urlWaypoint,
		type: 'GET',
		headers: {
			'Authorization':'Bearer ' + document.cookie,
		},
		success : function(data, textStatus, jqXHR ){
			var results = data;
			var waypoint;
			for (var i = 0; i < results.length; i++) {
				waypoint = results[i];
				// Marqueur
				var marker = new ol.Feature({
					geometry: new ol.geom.Point(
						ol.proj.fromLonLat([ waypoint.latitude, waypoint.longitude])
						),
					data : "Grade: " + waypoint.grade,
					header : "h1"
				});
				// Couleur
				/*marker.setStyle(new ol.style.Style({
					image: new ol.style.Icon(({
						color: '#ffcd46',
						crossOrigin: 'anonymous',
						src: 'dot.png'
					}))
				}));*/

				arrayMarker.push(marker);
			}
			fulfillMap();
		},

		error : function(jqXHR, statut, erreur){

		}
	});
}

function fulfillMap() {
	
	vectorSource = new ol.source.Vector({
		features: arrayMarker
	});

	vectorLayer = new ol.layer.Vector({
		source: vectorSource
	});

	map.addLayer(vectorLayer);
}

function colorMarker(grade) {

}