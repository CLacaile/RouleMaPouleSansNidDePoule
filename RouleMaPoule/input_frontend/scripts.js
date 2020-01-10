var vectorSource;

var vectorLayer;
var mapBackground;
var mapView;
var map;
var arrayMarker = new Array();

var url = 'http://localhost:8000/api/token/';

$('#Modal-login').modal({
	keyboard: false,
	backdrop: 'static',
	hide : false
});



$('#loginForm').submit(function(e){
	e.preventDefault();
	$.ajax({
		url: url,

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
		url: 'waypoint',
		dataType : 'json',
		headers: {
			'Authorization':'token ' + document.cookie,
		},
		method:'get',
		success : function(data, textStatus, jqXHR ){
			var results = data.results;
			var waypoint;
			for (var i = 0; i < results.length; i++) {
				waypoint = results[i];

				var marker = new ol.Feature({
					geometry: new ol.geom.Point(
						ol.proj.fromLonLat([ waypoint.latitude, waypoint.longitude])
						),
					data : "marker" + waypoint.id,
					header : "h1"
				});


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