// ==UserScript==
// @run-at document-end
// ==/UserScript==
console.clear();
document.querySelectorAll("#register-popup-bottom").forEach(e => e.remove());
document.querySelectorAll("#blocked-results-banner").forEach(e => e.remove());
for (let i = 0; i < 5; i++) {
	for(let item of document.getElementsByClassName('example blocked')){
		item.className = 'example';
	};
};
document.getElementById("pos-filters").scrollIntoView();