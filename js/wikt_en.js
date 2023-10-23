// ==UserScript==
// @run-at document-end
// ==/UserScript==
console.clear();
var mw_panel = document.getElementById('mw-panel');
var mw_body = document.getElementsByClassName('mw-body');
if (mw_body.length > 0) {
	console.log("Margin removed.");
	mw_panel.remove();
	mw_body[0].style.setProperty("margin-left","0","important")
	
	// set ipa transcription into variable
	var queryResult = document.querySelector("[href=\"/wiki/Appendix:French_pronunciation\"]");
	var ipa_transcription = "";
	if (queryResult != null) {
		IPA_element = queryResult.parentElement.parentElement.getElementsByClassName("IPA")[0];
		ipa_transcription = IPA_element.innerHTML;
	} else {
		console.log("IPA transcription not found.");
	};
	
	// scroll to first french result
	var query_french = document.querySelectorAll("strong[lang=\"fr\"]");
	if (query_french.length != 0) {
		query_french[0].parentElement.previousElementSibling.scrollIntoView(true);
	} else {
		console.log("Failed to find french entry.");
	};
};