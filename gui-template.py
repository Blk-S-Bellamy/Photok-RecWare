from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout, QTextEdit
)
from qt_material import apply_stylesheet
from PyQt6.QtCore import Qt
import sys
import cursed_clover as ccv
from cursed_clover import dupe_remove as cull
from cursed_clover import sync_folder as sync
import cc_storage as ccs
import os
from cc_ftp import ftp_ip
from PyQt6 import (QtGui, QtCore)


extra = {

    # Button colors
    'danger': '#ff3300',
    'warning': '#ffc107',
    'success': '#66ff66',

    # Font
    'font_family': 'Roboto',
}
## GLOBAL VARIABLES ##
scrape_now = False
scrape_webpages = []
chk_urls = [] 
chk_pathways = []


# primary loop for the program
def initialize_cc():
    # creates content directories and starts main function
    ccv.create_folder(ccv.root_path)
    ccv.create_folder(ccv.cache_path)


def def_checkthreads():
    scrape_webpages, archive_path = ccs.check_threads(scrape_webpages, archive_path)


def load_checkthreads():
    global chk_urls, chk_pathways
    chk_urls, chk_pathways = ccs.load_checkthreads()
    return chk_urls, chk_pathways


# save checkthreads and refresh from the source
def save_checkthread(url, pathway):
    ccs.add_checkthreads(url, os.path.join(ccv.root_path, pathway))
    chk_urls, chk_pathways = ccs.load_checkthreads()
    return chk_urls, chk_pathways


# make sure something was actually entered into the box
def check_url(url):
    if len(url.strip()) != 0:
        return True
    else:
        return False

class Window(QWidget):
    def __init__(self):
        super().__init__()
        global scrape_webpages, scrape_now
        self.resize(250, 250)
        self.setWindowTitle("Cursed Clover")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input = QLineEdit()
        self.input2 = QLineEdit()
        self.input.setFixedWidth(300)
        self.input.setClearButtonEnabled(True)
        self.input2.setClearButtonEnabled(True)
        self.input.setPlaceholderText("URL")
        self.input2.setPlaceholderText("Folder Name")
        self.input2.setFixedWidth(300)
        layout.addWidget(self.input, alignment= Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.input2, alignment= Qt.AlignmentFlag.AlignCenter)

        # button 1
        button1 = QPushButton("Add URL")
        button1.setProperty('class', 'success')
        button1.clicked.connect(self.get)
        button1.clicked.connect(self.input.clear)
        # button2
        button2 = QPushButton("scrape")
        button2.clicked.connect(self.save_all)
        button1.clicked.connect(self.input2.clear)
        # button3
        button3 = QPushButton("clear urls")
        button3.setProperty('class', 'danger')
        button3.clicked.connect(self.cls_chk)
        # adding all of the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        layout.addLayout(button_layout)
        # alignment= Qt.AlignmentFlag.AlignRight


        # button 1
        button4 = QPushButton("cull")
        button4.clicked.connect(cull)

        # ip box for the ftp server
        self.input4 = QLineEdit()
        self.input4.setClearButtonEnabled(True)
        self.input4.setPlaceholderText("FTP IP")
        self.input4.setFixedWidth(210)
        # button2
        button5 = QPushButton("sync")
        button5.clicked.connect(self.set_ftp_ip)
        button5.setProperty('class', 'success')

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(button5)
        button_layout2.addWidget(self.input4)
        layout.addLayout(button_layout2)

        # create terminal window to show term
        self.term = QTextEdit(self)
        self.term.setReadOnly(True)  # Make it read-only for output
        layout.addWidget(self.term)

        self.checkbox = QCheckBox("scrape now", self)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        footer = QHBoxLayout()
        footer.addWidget(button4)
        footer.addWidget(self.checkbox)
        layout.addLayout(footer)

    def get(self):
        global scrape_now
        url = self.input.text()
        pathway = self.input2.text()

        if scrape_now:
            self.append_output(f"SAVING:: 1 checkthread ({pathway})")
            self.save_one(url, pathway)

        if check_url(url):
            save_checkthread(url, pathway)
            self.append_output(f"ADDED:: 1 checkthread ({pathway})")
            print(f"ADDED:: 1 checkthread ({pathway})")
        else:
            self.append_output("(no input in url box, skipping...)")
            return

    def set_ftp_ip(self, ip):
        uin = self.input4.text()
        if len(uin) == 0:
            self.append_output("Failed to sync due to no ip being provided")
        # set ftp ip and sync to the ftp server
        else:
            try:
                ftp_ip = self.input4.text()
                sync(host=uin)
            except Exception as e:
                self.append_output(f"{e}")


    def cls_chk(self):
        urls = ccs.load_checkthreads()[0]
        ccs.clear_checkthreads()
        self.append_output(f"Deleted {len(urls)} entries in checkthreads")

    # determines if the entry should be scraped or appended
    def on_checkbox_changed(self):
        global scrape_now
        state = self.checkbox.checkState()
        if state == Qt.CheckState.Checked:
            print("enabled \"scrape now\"")
            self.append_output("enabled \"scrape now\"")
            scrape_now = True
        elif state == Qt.CheckState.Unchecked:
            print("disabled \"scrape now\"")
            self.append_output("disabled \"scrape now\"")
            scrape_now = False

    def append_output(self, text):
        """Append text to the output box."""
        self.term.append(text)

    def save_all(self):
        global chk_pathways, chk_urls
        chk_urls, chk_pathways = load_checkthreads()
        self.append_output(f"SCRAPING:: {len(chk_pathways)} urls...")
        ccv.fetch_all(chk_urls, chk_pathways)
        self.append_output(f"SCRAPED:: {len(chk_pathways)} urls...")

    # fetch one entry URL
    def save_one(self, url, pathway):
        self.append_output(f"SCRAPING:: 1 urls...")
        print(url, "", pathway)
        ccv.fetch_all([url], [pathway])
        self.append_output(f"SCRAPED:: 1 urls...")


app = QApplication(sys.argv)
app_icon = QtGui.QIcon()
app_icon.addFile('/home/browse/Downloads/Archives/SCMS/icons/50x50.png', QtCore.QSize(50,50))
app_icon.addFile('/home/browse/Downloads/Archives/SCMS/icons/100x100.png', QtCore.QSize(100,100))
apply_stylesheet(app, theme='dark_blue.xml', invert_secondary=True, extra=extra)
window = Window()
window.setWindowIcon(app_icon)
window.show()
app.exec()
# sys.exit(app.exec())