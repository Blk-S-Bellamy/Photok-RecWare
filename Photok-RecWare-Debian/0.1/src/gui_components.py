from PyQt6.QtWidgets import (
    QApplication, QSizePolicy, QWidget, QLabel, QLayout, QStyle, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
absolute_path = os.path.abspath(__file__)

class gbuttons():
    # dynamic button without fixed size
    def variable(title : str, colorclass='success'):
        button = QPushButton(title)
        button.setProperty('class', colorclass)
        return button

    # a button with a fixed size
    def fixed(title : str, colorclass='success', size=200):
        button = gbuttons.variable(title, colorclass=colorclass)
        button.setFixedWidth(size)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return button
    
    def checkbox(title : str, checked=True):
        box = QCheckBox(title)
        box.setChecked(True)
        box.setTristate(False)
        return box


# misc gui items
class other():
    # create a text box with default properties
    def textbox(title : str, width=350, clear=True):
        tbox = QLineEdit()
        tbox.setFixedWidth(width)
        tbox.setClearButtonEnabled(clear)
        tbox.setPlaceholderText(title)
        tbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return tbox

    # creates an image displayable on the gui
    def image(image_path : str):
        global absolute_path
        pixmap = QPixmap(image_path)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return label


class core():
    # read-only and can be appended to show what is going on
    def term(placeholder="", maxheight=200, maxwidth=2000):
        terminal = QTextEdit()
        terminal.setReadOnly(True)
        terminal.setPlaceholderText(placeholder)
        terminal.setMaximumHeight(maxheight)
        terminal.setMaximumWidth(maxwidth)
        terminal.setFontPointSize(12)
        terminal.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        return terminal


    def logo_term(logo_path : str, text : str, maxheight=75):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        syslog = core.term(placeholder="", maxheight=75, maxwidth=2000)
        syslog.append(text)

        # create widgets
        image = other.image(logo_path)
        
        layout.addWidget(image, stretch=0, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(syslog, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom)

        return layout


    
    # simply put something in a container and pass it back
    def boxthis(widget_, wid_spacing=10, vertical=True, alignment=Qt.AlignmentFlag.AlignBottom):
        if vertical:
            container = QVBoxLayout()
        else:
            container = QHBoxLayout()
        container.addWidget(widget_, alignment=alignment)
        container.setSpacing(wid_spacing)
        return container


class build():
    # construct a box with multiple text entries in it.
    def miscbox(nestme : list, wid_spacing=10, vertical=False, stretchlist=[], alignment=Qt.AlignmentFlag.AlignBottom):
        if vertical:
            layout = QVBoxLayout()
        else:
            layout = QHBoxLayout()

        layout.setSpacing(wid_spacing)
        constructed = {}
        try:
            for count, thing in enumerate(nestme):
                # Will nest the objects if they are widget or layouts
                if isinstance(thing, QWidget):
                    if len(stretchlist) >= 1:
                        layout.addWidget(thing, stretch=stretchlist[count], alignment=alignment)
                    else:
                        layout.addWidget(thing, alignment=alignment)
                elif isinstance(thing, QLayout):
                    if len(stretchlist) >= 1:
                        layout.addLayout(thing, stretch=stretchlist[count])
                    else:
                        layout.addLayout(thing)
                    # layout.addLayout(thing)
                else:
                    print("Unknown type", thing)
        except Exception as e:
            print(e)
            return layout
        return layout

    # put buttons in a box, dawg
    def buttonbox(buttons : list, btn_size=200, btn_stretch=False, wid_spacing=10, vertical=False, alignment=Qt.AlignmentFlag.AlignBottom):
        constructed = {}
        tbb = []
        try:
            for thing in buttons:
                if btn_stretch:
                    btn = gbuttons.variable(thing)
                else:
                    btn = gbuttons.fixed(thing, size=btn_size)
                tbb.append(btn)
                constructed[thing] = btn
        except Exception as e:
            print(e)
        final_layout = build.miscbox(tbb, wid_spacing=wid_spacing, vertical=vertical, alignment=alignment)
        return final_layout, constructed

    def textbox_box(titles : list, width=350, clear=True, wid_spacing=10, vertical=False, alignment=Qt.AlignmentFlag.AlignBottom):
        constructed = {}
        tbb = []
        try:
            for thing in titles:
                    box = other.textbox(thing, width=width, clear=clear)
                    tbb.append(box)
                    constructed[thing] = box
        except Exception as e:
            print(e)
        final_layout = build.miscbox(tbb, wid_spacing=wid_spacing, vertical=vertical, alignment=alignment)

        return final_layout, constructed

    def checkbox_box(checkboxes : list, wid_spacing=10, vertical=False, setChecked=True, alignment=Qt.AlignmentFlag.AlignBottom):
        constructed = {}
        tbb = []
        try:
            for thing in checkboxes:
                    box = gbuttons.checkbox(thing, checked=setChecked)
                    tbb.append(box)
                    constructed[thing] = box
        except Exception as e:
            print(e)
        final_layout = build.miscbox(tbb, wid_spacing=wid_spacing, vertical=vertical, alignment=alignment)

        return final_layout, constructed