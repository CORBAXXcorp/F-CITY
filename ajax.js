'use strict';

//------------------------------------------------------------------
//--- ajaxRequest --------------------------------------------------
//------------------------------------------------------------------
// Fonction qui communique avec le serveur grâce au protocole HTTP
// \param type Type de méthode de la requête
// \param url Contient l'url vers la ressource
// \param callback Fonction appelé si la requête renvoie un bon code
// \param data Contient les paramètres supplémentaires
// \return Renvoie la réponse du serveur décodé à la fonction de callback
function ajaxRequest(type, url, callback, data = null) {
	let xhr = new XMLHttpRequest();			// Création d'un nouveau protocole Http
	if (type == 'GET' && data != null) {
		url += '?' + data;
	}
	xhr.open(type, url);
	// Header prenant en compte le formalisme REST
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	console.log(url); // Regarde l'url envoyé

	xhr.onload = () => {
		console.log(xhr.responseText); // Regarde la réponse quoi qu'il arrive 
		// En fonction du code de retour, on effectue quelque chose
		switch(xhr.status) {
			case 200:
			case 201:
				if (xhr.responseText.length != 0) {callback(JSON.parse(xhr.responseText));}
				else {callback(null);}
				break;
			default: 
				httpErrors(xhr.status);
		}
	};
	console.log(data); // Regarde les paramètres passés
	xhr.send(data);
}

//------------------------------------------------------------------
//--- httpErrors ---------------------------------------------------
//------------------------------------------------------------------
// Affiche dans la console une courte description de l'erreur
// \param errorCode Contient le code erreur HTTP
function httpErrors(errorCode) {
	let message = {
		400: '400: Requête incorrecte',
		401: '401: Authentifiez-vous',
		403: '403: Accès refusé',
		404: '404: Bad request',
		500: '500: Erreur interne au Serveur',
		503: '503: Service indisponible'
	}
	console.log(message[errorCode]); // Affiche l'erreur
}

var startTime = 0
var start = 0
var end = 0
var diff = 0
var timerID = 0
window.onload = chronoStart;
function chrono(){
	end = new Date()
	diff = end - start
	diff = new Date(diff)
	var msec = diff.getMilliseconds()
	var sec = diff.getSeconds()
	var min = diff.getMinutes()
	var hr = diff.getHours()-1
	if (min < 10){
		min = "0" + min
	}
	if (sec < 10){
		sec = "0" + sec
	}
	if(msec < 10){
		msec = "00" +msec
	}
	else if(msec < 100){
		msec = "0" +msec
	}
	document.getElementById("chronotime").value = hr + ":" + min + ":" + sec
	timerID = setTimeout("chrono()", 10)
}
function chronoStart(){
	document.chronoForm.startstop.value = "stop"
	document.chronoForm.startstop.onclick = chronoStop
	document.chronoForm.reset.onclick = chronoReset
	start = new Date()
	chrono()
}
function chronoContinue(){
	document.chronoForm.startstop.value = "stop"
	document.chronoForm.startstop.onclick = chronoStop
	document.chronoForm.reset.onclick = chronoReset
	start = new Date()-diff
	start = new Date(start)
	chrono()
}
function chronoReset(){
	document.getElementById("chronotime").value = "0:00:00:000"
	start = new Date()
}
function chronoStopReset(){
	document.getElementById("chronotime").value = "0:00:00:000"
	document.chronoForm.startstop.onclick = chronoStart
}
function chronoStop(){
	document.chronoForm.startstop.value = "start!"
	document.chronoForm.startstop.onclick = chronoContinue
	document.chronoForm.reset.onclick = chronoStopReset
	clearTimeout(timerID)
}