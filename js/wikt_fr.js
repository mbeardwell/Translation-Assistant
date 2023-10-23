// ==UserScript==
// @run-at document-end
// ==/UserScript==
console.clear();
document.getElementById('mw-panel').remove();
document.getElementsByClassName('mw-content-container')[0].style.marginLeft='0';
// delete pronunciation box to prevent canadian transcriptions being read
document.getElementById('Prononciation').parentElement.nextSibling.nextSibling.remove()

var query = document.querySelectorAll("a[href=\"/wiki/Annexe:Prononciation/fran%C3%A7ais\"]");
var transcriptions = [];
if (query.length > 0) {
	[...query].forEach(x=>transcriptions.push(x.firstElementChild.innerText));
}; 
transcriptions = JSON.stringify(transcriptions);

document.getElementsByClassName('titredef')[0].scrollIntoView(true);