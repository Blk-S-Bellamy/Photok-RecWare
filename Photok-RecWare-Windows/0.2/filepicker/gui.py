#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# IMPORTS
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

# gui widget imports
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QSizePolicy,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QDialog
)
# dark mode styling for the pyqt6 application and other styling imports
from qt_material import apply_stylesheet
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6 import (QtGui, QtCore)
from pathlib import Path
import sys
import os
from filepicker.dirtools import DirEngine as DE

# activate a filebrowser instance with ability to see any files
fbrowser = DE(mode='any')
fbapp = None
mode = None
failed = True
closeme = None
HOME_PATH = str(Path.home())

#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# GLOBALS
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

absolute_path = os.path.dirname(os.path.abspath(__file__))
logo = os.path.join(absolute_path, 'icons', 'folder-sapphire-backup.png')
fol_icon = os.path.join(absolute_path, 'icons', 'folder.png')
fil_icon = os.path.join(absolute_path, 'icons', 'filename-title-amarok.png')
backup_icon = os.path.join(absolute_path, 'icons', 'grsync-restore.png')
left_arrow = os.path.join(absolute_path, 'icons', 'arrow-left.png')
right_arrow = os.path.join(absolute_path, 'icons', 'arrow-right.png')
up_arrow = os.path.join(absolute_path, 'icons', 'arrow-up.png')
gui_patchbay = {}  # contains relevant widget update hooks

#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# PYQT6 STYLING
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

# applied as a style sheet and modernize gui somewhat
extra = {
    # Button colors
    'danger': '#ff3300',
    'warning': '#ffc107',
    'success': '#66ff66',
    # Font
    'font_family': 'Roboto',
}


# misc gui items
class other():
    def inform_user():
        global fbrowser, logo
        if fbrowser.lasterror != "":
            msgBox = QMessageBox()
            msgBox.setText(fbrowser.lasterror)
            msgBox.setWindowTitle('you made an oopsie :P')
            msgBox.setIcon(QMessageBox.Icon.Warning)
            fbrowser.lasterror = ""
            msgBox.exec()

    # create a text box with default properties
    def textbox(title : str, width=350, clear=True):
        tbox = QLineEdit()
        tbox.setFixedWidth(width)
        tbox.setClearButtonEnabled(clear)
        tbox.setPlaceholderText(title)
        tbox.setFont(QFont('Helvetica', 25))
        tbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return tbox

    def validate_pathbox():
        tbox = gui_patchbay['pathbox']
        try:
            if os.path.isdir(tbox.text()):
                fbrowser.cd(tbox.text())
                other.fb_update()
            else:
                pass
        except Exception as e:
            pass

    def set_selected():
        global gui_patchbay, fbrowser
        try:
            report = gui_patchbay['selectedbox']
            view = gui_patchbay['view2']
            selection = os.path.join(fbrowser.current, view.currentItem().text())
            fbrowser.selected = selection
            report.setText(str(selection))
        except Exception:
            pass

    # changes the icon for backup folders to be different
    def backup_check():
        global backup_icon
        view = gui_patchbay['view2']
        found = []
        folders = fbrowser.filter_type(mode='directories')

        try:
            for count, item in enumerate(folders):
                try:
                    dirlist = os.listdir(os.path.join(fbrowser.current, item))
                    extensions = [os.path.splitext(i)[1] for i in dirlist]
                    if '.photok' in extensions or '.meta' in extensions:
                        found.append(item)
                        del folders[count]
                except PermissionError:
                    pass
            # generate the list items with a backup icon
            backups = fbbuild.filelist_add_icon(found, backup_icon)
            view = fbbuild.filelist_add_items(view, backups)
        except ValueError as e:
            print(e)
        return folders

    # updates the file view based on the current position 
    def fb_update():
        view = gui_patchbay['view2']
        files = fbbuild.filelist_add_icon(fbrowser.filter_type(mode='files'), fil_icon)
        view.clear()
        folders = other.backup_check()
        folders = fbbuild.filelist_add_icon(folders, fol_icon)
        view = fbbuild.filelist_add_items(view, folders)
        view = fbbuild.filelist_add_items(view, files)
        other.update_pathbox()

    # change directories to the double-clicked item
    def doubleclick_cd():
        global gui_patchbay, fbrowser
        view = gui_patchbay['view2']
        selection = view.currentItem().text()
        if os.path.isdir(os.path.join(fbrowser.current, selection)):
            newdir = os.path.join(fbrowser.current, selection)
            fbrowser.cd(newdir)
            other.inform_user()
            other.fb_update()

    def update_pathbox():
        global fbrowser
        view = gui_patchbay['pathbox']
        view.setText(fbrowser.current)

    # change directories to the double-clicked item in view 1
    def master_cd():
        global gui_patchbay, fbrowser, HOME_PATH
        view = gui_patchbay['view1']
        selection = view.currentItem().text()
        if os.path.isdir(os.path.join(HOME_PATH, selection)):
            newdir = os.path.join(HOME_PATH, selection)
            fbrowser.cd(newdir)
            other.fb_update()

    # when triggered, goes back one in history
    def backdir():
        global gui_patchbay, fbrowser
        fbrowser.back()
        other.fb_update()

    # when triggered, goes back one in history
    def forwarddir():
        global gui_patchbay, fbrowser
        fbrowser.forward()
        other.fb_update()

    # when triggered, goes back one in history
    def updir():
        global gui_patchbay, fbrowser
        fbrowser.up()
        other.fb_update()

    def select():
        global mode, failed
        try:
            if mode == 'directory':
                if os.path.isdir(fbrowser.selected):
                    failed = False
                    closeme()
                else:
                    print('not a directory  :/')
            elif mode == 'file':
                    if os.path.isfile(fbrowser.selected):
                        failed = False
                        closeme()
                    else:
                        print('not a file  :/')
            elif mode == 'any':
                if os.path.isfile(fbrowser.selected) or os.path.isdir(fbrowser.selected):
                        failed = False
                        closeme()
                else:
                    print('not a file or directory :/')
            else:
                print(f'not a valid mode for selection "{mode}"')
        except Exception:
            pass

    def enter_select():
        global gui_patchbay
        try:
            tbox = gui_patchbay['selectedbox']
            fbrowser.selected = tbox.text()
            other.select()
        except Exception as e:
            print(e)

# contains all button linking configurations, centralized button attachments
class fbpatchbay():
    # append a component to the patchbay with a reference name
    def append(component_name : (str, list), element : (str, list), overwrite=True):
        # reduces code complexit with nested logic
        def go(component_name : (str, list), element, overwrite=True):
            global gui_patchbay
            if overwrite:
                gui_patchbay[component_name] = element
            else:
                try:
                    gui_patchbay[component_name]
                except KeyError:
                    gui_patchbay[component_name] = element
            return

        # handle list and string datatypes
        if type(component_name) == list:
            for count, item in enumerate(component_name):
                go(item, element[count], overwrite=overwrite)
        else:
            go(component_name, element, overwrite=overwrite)


    # attach a button press to a function by button reference name
    def attach_listpress(list_name, link):
        global gui_patchbay
        try:
            component = gui_patchbay[list_name]
        except ValueError as e:
            print(f'Failed to find and connect button... {e}')


    # attach a button press to a function by button reference name
    def attach_button(button_name, link):
        global gui_patchbay
        try:
            component = gui_patchbay[button_name]
            component.clicked.connect(link)
        except Exception as e:
            print(f'Failed to find and connect button... {e}')

    # attach a checkbox state change to a function by reference name
    def attach_checkbox(checkbox_name, link):
        global gui_patchbay
        try:
            checkbox = gui_patchbay[checkbox_name]
            checkbox.stateChanged.connect(link)
        except Exception as e:
            print(f'{e}')


# used to map actions to functions for the gui
class actions():
    def mappall():
        global fbrowser, gui_patchbay
        try:
            component = gui_patchbay['view2']
            component.itemSelectionChanged.connect(other.set_selected)
            component.itemDoubleClicked.connect(other.doubleclick_cd)

            hback = gui_patchbay['lnav']
            hback.clicked.connect(other.backdir)

            hback = gui_patchbay['rnav']
            hback.clicked.connect(other.forwarddir)

            hback = gui_patchbay['unav']
            hback.clicked.connect(other.updir)

            component = gui_patchbay['view1']
            component.itemDoubleClicked.connect(other.master_cd)

            sel = gui_patchbay['select']
            sel.clicked.connect(other.select)

            pathbox = gui_patchbay['pathbox']
            pathbox.textChanged.connect(other.validate_pathbox)

            selectedbox = gui_patchbay['selectedbox']
            selectedbox.returnPressed.connect(other.enter_select)

        except Exception as e:
            print(e)


# constructor functions for the file browser buttons
class fbbuild():
    # create a text box with default properties
    def textbox(title : str, width=350, clear=True):
        tbox = QLineEdit()
        tbox.setFixedWidth(width)
        tbox.setClearButtonEnabled(clear)
        tbox.setText(title)
        tbox.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return tbox

    # dynamic button without fixed size
    def btn_variable(title : str, colorclass='success'):
        button = QPushButton(title)
        button.setProperty('class', colorclass)
        return button

    # a button with a fixed size
    def btn_fixed(title : str, colorclass='success', size=200):
        button = fbbuild.btn_variable(title, colorclass=colorclass)
        button.setFixedWidth(size)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return button

    # a button with a fixed size
    def btn_img(image : str, colorclass='null', size=50):
        try:
            btn = QPushButton()
            btn.setIcon(QIcon(image))
            btn.setProperty('class', colorclass)
            btn.setFixedWidth(size)
        except Exception as e:
            print(e)
            return fbbuild.btn_fixed('failed', size=100)
        return btn
    
    def filelist_add_icon(items : list, icon : str):
        finished = []
        try:
            for item in items:
                icon = QIcon(icon)  # Provide the path to your icon file
                entry = QListWidgetItem(icon, item)
                entry.setFont(QFont('Helvetica', 15))
                finished.append(entry)
        except Exception as e:
            print(e)
            return items
        return finished

    # add multiple icon entries in one call
    def filelist_add_items(widg, entries):
        for line in entries:
            try:
                widg.addItem(line)
            except Exception as e: 
                print(e)
        return widg

    # displays files or folders for choosing/selecting
    def filelist(items=[], maxheight=None, maxwidth=None, alternate_colors=True):
        try:
            fblist = QListWidget()
            if alternate_colors:
                fblist.setAlternatingRowColors(True)
            if len(items) != 0:
                fblist.addItems(items)
            

            if maxheight != None:
                for i in range(fblist.count()):
                    item = fblist.item(i)
                    fblist.item(i).setSizeHint(QSize(item.sizeHint().width(), maxheight))
            if maxwidth != None:
                fblist.setFixedWidth(maxwidth)

            return fblist
        except Exception as e:
            print(e)


# combine widget constructors to make bigger components
class fbcomponents():
    def nav_buttons():
        # compose the navigation buttons
        global left_arrow, right_arrow, up_arrow
        left = fbbuild.btn_img(left_arrow, size=40)
        right = fbbuild.btn_img(right_arrow, size=40)
        up = fbbuild.btn_img(up_arrow, size=40)
        select = fbbuild.btn_fixed('Select', size=200)
        return left, right, up, select


    def core_lists():
        global fol_icon, fil_icon, fbrowser
        widg = fbbuild.filelist(fbrowser.filter_type(mode='directories'), maxwidth=175)
        widg2 = fbbuild.filelist(alternate_colors=False)
        return widg, widg2
    
    def boxes():
        global fbrowser
        pathbox = fbbuild.textbox(fbrowser.current, width=500)
        selectedbox = fbbuild.textbox(fbrowser.current, width=300)
        return pathbox, selectedbox

# components combined into pages/windows 
class pages():
    def main():
        view1, view2 = fbcomponents.core_lists()
        left, right, up, select = fbcomponents.nav_buttons()
        pathbox, selectedbox = fbcomponents.boxes()

        # add to the patchbay for easy configuration and updating later
        fbpatchbay.append(['pathbox', 'selectedbox', 'select'], [pathbox, selectedbox, select])
        fbpatchbay.append(['view1', 'view2', 'lnav', 'rnav', 'unav'], [view1, view2, left, right, up])
        other.fb_update()
        # nav buttons
        nav_btns = QHBoxLayout()
        nav_btns.addWidget(left, alignment=Qt.AlignmentFlag.AlignCenter)
        nav_btns.addWidget(right, alignment=Qt.AlignmentFlag.AlignCenter)
        nav_btns.addWidget(up, alignment=Qt.AlignmentFlag.AlignCenter)

        # create left of the page
        v1 = QVBoxLayout()
        v1.addLayout(nav_btns)
        v1.addWidget(view1)

        # submit and selected file box
        sub_btns = QHBoxLayout()
        sub_btns.addWidget(selectedbox, alignment=Qt.AlignmentFlag.AlignCenter)
        sub_btns.addWidget(select, alignment=Qt.AlignmentFlag.AlignCenter)

        # build the right of the page
        v2 = QVBoxLayout()
        v2.addWidget(pathbox, alignment=Qt.AlignmentFlag.AlignCenter)
        v2.addWidget(view2)
        v2.addLayout(sub_btns)

        layout = QHBoxLayout()
        layout.addLayout(v1)
        layout.addLayout(v2)
        return layout


#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# BUILD APPLICATION AND LAUNCH
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 500)
        self.setWindowTitle("Pick a Folder *~* ")
        # add major components
        self.setLayout(pages.main())
        actions.mappall()


# run the file chooser
# modes: directory, file, any
def runapp(select_type='directory'):
    global fbapp, fbrowser, mode, failed
    try:
        mode = select_type
        fbapp = QApplication(sys.argv)
        closeme = fbapp.quit
        app_icon = QtGui.QIcon()
        apply_stylesheet(fbapp, theme='dark_teal.xml', invert_secondary=False, extra=extra)
        app_icon.addFile(logo, QtCore.QSize(50,50))
        app_icon.addFile(logo, QtCore.QSize(100,100))
        window = Window()
        window.setWindowIcon(app_icon)
        window.setWindowOpacity(0.95)
        window.show()
        fbapp.exec()
    except Exception as e:
        print(e)
        failed = True
        
    if failed:
        return ""
    else:
        return fbrowser.selected

# choose a folder as a windows not an app
def choose_folder(title='Choose a Folder *~* '):
    global fbapp, fbrowser, mode, failed, closeme
    try:
        mode = 'directory'
        page = QDialog()
        page.setWindowTitle(title)
        page.setLayout(pages.main())
        page.setWindowOpacity(0.95)
        page.resize(300, 500)
        actions.mappall()
        fbapp = page
        closeme = page.accept

        fbrowser.update_contents()
        other.fb_update()

        page.exec()
    except Exception as e:
        print(e)
        failed = True
        
    if failed:
        return ""
    else:
        return fbrowser.selected

