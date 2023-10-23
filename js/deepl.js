// ==UserScript==
// @run-at document-idle
// ==/UserScript==
console.clear();
console.log("Deepl script initiated.");

// remove cookie 'accept'/'accept all' box
var cookieBanner = document.getElementById('dl_cookieBanner');
if (cookieBanner != null) {cookieBanner.remove();};
// remove sticky header
for (let item of document.getElementsByClassName('dl_header dl_header--sticky')) {
		item.remove();
};

// wait for generation of translations
// https://stackoverflow.com/questions/16149431/make-function-wait-until-element-exists/47776379
var checkExist = setInterval(function() {
   var translation = document.querySelectorAll(("button[class=\"lmt__translations_as_text__text_btn\"]"))[0].innerText
   var translation_examples = document.getElementsByClassName('isForeignTerm');
   if (translation.length > 1 && translation_examples.length > 0) {
      console.log("Primary translation: ",translation)
      console.log("Translations generated.");
	  console.log("Translation examples: ");
	  console.log(translation_examples);
	  formatPage();
      clearInterval(checkExist);
   }
}, 50); // check every 100ms

function formatPage() {
var tickMark = document.querySelectorAll('lt-toolbar[contenteditable="false"][data-lt-force-appearance="light"][style="display: none;"]');
if (tickMark.length > 0) {tickMark[0].remove();};

for (let item of document.getElementsByClassName('lmt__docTrans-tab-container')) {
		item.remove();
};
document.getElementById('lmt_pro_ad_container_1')
		.remove();
document.getElementById('lmt_pro_ad_container_2')
		.remove();
document.getElementById('lmt_quotes_article')
		.remove();
for (let item of document.getElementsByClassName('dl_footer')) {
		item.remove();
};

var query = "div[dl-test = \"translator-source\"][class = \"lmt__side_container lmt__side_container--source\"]"
Array.prototype.forEach.call(document.querySelectorAll(query), x => x.remove());
Array.prototype.forEach.call(document.getElementsByClassName('lmt__language_container_switch'),x => x.remove());
Array.prototype.forEach.call(document.getElementsByClassName('lmt__language_container'),x => x.remove());
document.getElementById('dl_translator')
		.style.paddingLeft = 0;
document.querySelector('[class = \"lmt__target_toolbar lmt__target_toolbar--visible\"]')
		.remove();

var class_name = '\"lmt__textarea_container df1966__increase_padding lmt__df-1851_raise_alternatives_placement\"'
// var temp = document.querySelector('[class = ' + class_name + ']');
var temp = document.getElementsByClassName('lmt__textarea_container');
if (temp == null || temp.length == 0 ) {
		console.log("Temp null at flag 1");
} else {
		Array.prototype.forEach.call(temp,x => x.style.paddingLeft = 0);
		Array.prototype.forEach.call(temp,x => x.style.paddingTop = 0);
		Array.prototype.forEach.call(temp,x => x.style.paddingRight = 0);
		Array.prototype.forEach.call(temp,x => x.style.paddingBottom = 0);
};

Array.prototype.forEach.call(document.getElementsByClassName('lmt__textarea_container'), x => (x.style.minHeight = 0));
document.querySelector("[dl-test = \"translator-target-result-as-text-container\"]")
		.style.paddingLeft = 0;

var translations = []
Array.prototype.forEach.call(document.querySelectorAll("button[class=\"lmt__translations_as_text__text_btn\"]"),x => {
				if (!translations.includes(x.innerText) && !x.innerText.includes(" .")) {
						translations.push(x.innerText);
				}
		});
translations = translations.sort();
translations = translations.join(", ");
console.log("Translations: " + translations)
var style = "margin-top: 5px; margin-bottom: 5px; margin-left: 5px; font-size: 25px;";
var translations_div = "<div class=\"lmt__dict\" style=\"" + style + "\">" + translations + "</div>";
document.body.innerHTML = translations_div + document.body.innerHTML;

Array.prototype.forEach.call(document.getElementsByClassName('lmt__sides_container'),x => x.remove());
document.getElementById('dl_translator')
		.style.paddingTop = 0;

temp = document.getElementsByClassName('lmt__dict__inner')[0];
temp.style.paddingLeft = "5px";
temp.style.paddingRight = "5px";
temp.style.paddingTop = 0;
temp.style.paddingBottom = 0;

temp = document.getElementById('lmt__dict');
temp.style.marginTop = "5px";
temp.style.marginLeft = "5px";
temp.style.marginRight = "5px";
temp.style.marginBottom = "5px";

Array.prototype.forEach.call(document.getElementsByClassName('lmt__dict__inner'),x => x.style.boxShadow = "0px 0px 0px rgb(0 0 0 / 0%)");
Array.prototype.forEach.call(document.getElementsByClassName('dl_body'),x => x.style.setProperty("background-color", "white", "important"));

temp = document.getElementsByClassName('exact')[0];
if (temp == null) {
		console.log("Temp null at flag 3");
} else {
		temp.style.setProperty("border-style", "solid", "important");
		temp.style.setProperty("border-color", "white", "important");
		temp.style.setProperty("border-top-width", "2px", "important");
		temp.style.setProperty("border-top-color", "black", "important");
};
scrollTo(0, 0);
};