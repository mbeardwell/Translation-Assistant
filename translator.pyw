#!/usr/bin/python3.10
import json
import sys
import os
import sys
from urllib.parse import quote

from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

# Apply Linux-only fixes
if sys.platform.startswith("linux"):
    os.environ["QT_QPA_PLATFORM"] = "xcb" # Forces X11 (fixes Wayland/Chromebook)

def read_source(relative_source_path):
    proj_root = os.path.dirname(os.path.abspath(__file__))
    abs_source_path = proj_root + "/" + relative_source_path
    return ''.join(open(abs_source_path, "r", encoding="utf-8").readlines())

class TranslationPageElementBase:
    def __init__(self, name, height, js_path, query_base_url, fragment=None, load_finished_callback=None):
        self.webengine_view = QWebEngineView()

        self.webengine_script = QWebEngineScript()
        self.webengine_script.setWorldId(QWebEngineScript.MainWorld)
        self.webengine_script.setSourceCode(read_source(js_path))
        self.webengine_script.setInjectionPoint(QWebEngineScript.Deferred)
        self.profile = QWebEngineProfile(name, self.webengine_view)
        self.profile.scripts().insert(self.webengine_script)

        self.fragment = fragment
        self.window_height = height
        self.query_base_url = query_base_url

        if load_finished_callback is not None:
            self.webengine_view.loadFinished.connect(load_finished_callback)

    def load_search(self, search_text):
        self.webengine_view.page().deleteLater()
        self.webengine_view.setPage(QWebEnginePage(self.profile, self.webengine_view))

        url = QUrl(self.query_base_url + search_text)

        if self.fragment is not None:
            url.setFragment(self.fragment)

        self.webengine_view.load(url)


class TranslationPageElement(TranslationPageElementBase):
    def __init__(self, name, height, js_path, query_base_url, fragment=None):
        super().__init__(name, height, js_path, query_base_url, fragment=fragment)


class TranslationPageElementWiktFr(TranslationPageElementBase):
    def __init__(self, name, height, js_path, query_base_url, fragment=None, searchbar_obj=None):
        super().__init__(name, height, js_path, query_base_url,
                         fragment=fragment,
                         load_finished_callback=self.handle_wikt_fr_loaded)

        self.ipa_callback_obj = searchbar_obj

    """
    GET IPA STRING
    e.g. returns <span class="API" title="Prononciation API">\\a ak.sɑ̃ ɡʁav\\</span>
    """

    def handle_wikt_fr_loaded(self):
        self.webengine_view.page().runJavaScript("transcriptions;",
                                                 QWebEngineScript.MainWorld,
                                                 self.ipa_callback_obj.set_ipa)


class TranslationSearchbar(QWidget):
    def __init__(self, callback_obj):
        super().__init__()
        self.FONT_SIZE = 20
        self.callback_obj = callback_obj

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.textbox = QLineEdit()
        self.textbox.setPlaceholderText("Search... ")
        self.textbox.returnPressed.connect(self.handle_return_pressed)
        self.textbox.font().setPointSize(self.FONT_SIZE)
        self.layout.addWidget(self.textbox, alignment=Qt.AlignRight)

        self.IPA_Label = QLabel()
        self.IPA_Label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout.addWidget(self.IPA_Label, alignment=Qt.AlignRight)

    def focus(self):
        self.textbox.setFocus()

    def handle_return_pressed(self):
        print("Return pressed. Searching >>> " + self.textbox.displayText())
        self.IPA_Label.setText("")  # remove IPA transcription
        search_string = quote(self.textbox.displayText())
        self.callback_obj.load_search(search_string)

    def set_ipa(self, ipa):
        if ipa is None:
            print("IPA received is None")
            return

        ipa = json.loads(ipa)
        ipa = list(set(ipa))
        print("IPA transcription received: ", ipa)
        try:
            fixed_ipas = []
            for e in ipa:
                fixed_ipas.append(e[1:-1])  # removing surrounding / / or \ \
            fixed_ipas.sort()
            fixed_ipas = list(set(fixed_ipas))
            ipa_text = ', '.join(fixed_ipas)
            print(ipa_text)
            self.IPA_Label.setText(ipa_text)
        except Exception as err:
            print(err)


class Translator(QWidget):
    SUPPORTED_LANGS = ["en", "de", "fr", "nl", "it"]

    def __init__(self):
        super().__init__()
        self.DEFAULT_WIDTH = 480
        self.DEFAULT_HEIGHT = 480
        self.WEB_MIN_HEIGHT = 700

        self.selfLayout = QVBoxLayout()
        self.setLayout(self.selfLayout)
        self.topbar = QHBoxLayout()
        self.selfLayout.addLayout(self.topbar)

        # Button
        widget = QWidget()
        self.btn = QPushButton("Big Mode", widget)
        self.btn.setCheckable(True)
        self.btn.setFixedSize(100, 50)
        self.btn.clicked.connect(self.handle_big_mode_toggle)
        self.topbar.addWidget(self.btn)

        # Search bar
        self.searchbar = TranslationSearchbar(self)
        self.topbar.addWidget(self.searchbar)

        # Search results
        self.webpages_layout = QVBoxLayout()
        self.selfLayout.addLayout(self.webpages_layout)
        self.pages = []
        self.pages.append(TranslationPageElement("wikt_en", 50, "js/wikt_en.js",
                                                 self.get_url_wikt("en")))
        self.pages.append(TranslationPageElementWiktFr("wikt_fr", 50, "js/wikt_fr.js",
                                                       self.get_url_wikt("fr"),
                                                       fragment="Français",
                                                       searchbar_obj=self.searchbar))
        self.pages.append(TranslationPageElement("deepl", 45, "js/deepl.js",
                                                 self.get_url_deepl("fr")))
        self.pages.append(TranslationPageElement("reverso", 45, "js/reverso.js",
                                                 self.get_url_reverso("fr")))

        for p in self.pages:
            self.webpages_layout.addWidget(p.webengine_view, p.window_height)

        self.searchbar.focus()


        self.height, self.width = self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT

    def check_supported(self, lang):
        if lang not in Translator.SUPPORTED_LANGS:
            print("Unsupported language -",lang)
            sys.exit(1)

    def get_url_wikt(self, lang):
        self.check_supported(lang)
        return "https://{}.wiktionary.org/w/index.php?search=".format(lang)

    def get_url_deepl(self, lang):
        self.check_supported(lang)
        return "https://www.deepl.com/translator#{}/en/".format(lang)

    def get_url_reverso(self, lang):
        self.check_supported(lang)
        lang_translated = {"fr": "french", "nl":"dutch", "it":"italian", "de":"german"}
        return "https://context.reverso.net/translation/{}-english/".format(lang_translated[lang])

    def load_search(self, search_string):
        for p in self.pages:
            p.load_search(search_string)

    def handle_big_mode_toggle(self):
        for p in self.pages[2:]:
            p.webengine_view.setVisible(not p.webengine_view.isVisible())


app = QApplication(['', '--no-sandbox'])  # TODO investigate why/if removing sandbox is needed
window = Translator()
window.setGeometry(QRect(0, 0, 1000, 1000))
window.setWindowTitle("French to English Translation Aide")
window.show()
sys.exit(app.exec_())
