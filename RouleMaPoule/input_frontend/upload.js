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
			
		},

		error : function(jqXHR, statut, erreur){

		}
	});
});
