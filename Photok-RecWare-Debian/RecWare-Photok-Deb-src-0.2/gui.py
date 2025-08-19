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
    QCheckBox,
    QHBoxLayout,
    QTextEdit,
    QLabel,
    QSizePolicy,
    QDialog,
    QFrame,
    QFileIconProvider
)
# dark mode styling for the pyqt6 application and other styling imports
from qt_material import apply_stylesheet
from PyQt6.QtGui import QPainter, QColor, QFont, QIcon
from PyQt6.QtCore import Qt
from PyQt6 import (QtGui, QtCore)
import sys
import os
from filepicker import gui as fgui
# currently selected backup and other relevant data
current_backup = {'path' : '',
                  'files' : [],
                  'metadata' : {},
                  'bcrypt' : ''}
# checkbox-linked options for when trying to decrypt files
decrypt_options = {'restore_filenames' : True,
                   'restore_albumnames' : True,
                   'restore_albums' : True
                   }
# custom gui module imports
import gui_components as gcomp
import engine.pkboilerplate as bp
from engine import pkcore as core
from engine import pkcrypto as pkc
from gui_lookmaxing import styles
import pkmiscdata as misc
# globals
HOME_PATH = os.getenv("HOME")
# contains checkbox instances for checking status
checkbx = {}
# contains hooks for graphical elements such as buttons and boxes
gui_patchbay = {}

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

#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# MISC
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#


# ensure the backup information is reset between backups
def reset_backup():
    current_backup['path'] = ''
    current_backup['files'] = []
    current_backup['metadata'] = {}
    current_backup['bcrypt'] = ''


# logic behind each gui widget/component
class component_functions():
    # yea, just sets the backup lmao
    def set_backup():
        global HOME_PATH, current_backup, current_backup_res
        reset_backup()  # reset backup information
        component_functions.append_action_log(f'choosing backup...')

        pathway = fgui.choose_folder()

        if pathway == "":
            return
        elif len(pathway) == 0:
            return
        else:
            if type(pathway) == list:
                pathway = pathway[0]

        current_backup['path'] = pathway
        component_functions.display_metadata()

        # try to add backup information
        try:
            metadata = core.backup.load_meta(os.path.join(pathway, 'meta.json'))
            if metadata == {}:
                pass
            else:
                current_backup['metadata'] = metadata
                current_backup['bcrypt'] = metadata['password']
        except Exception as e:
            pass

    # reverses the boolean value of a given checkbox
    def switch_checkbox(checkbox_name):
        global gui_patchbay
        try:
            checkbox = gui_patchbay[checkbox_name]
            if checkbox.isChecked():
                checkbox.setChecked(False)
            else:
                checkbox.setChecked(True)
        except Exception:
            pass

    # simple logic to toggle/invert a buttons stored value
    def invert_decrypt_option(option):
        global decrypt_options
        try:
            checkbox = decrypt_options[option]
            if checkbox is True:
                decrypt_options[option] = False
            else:
                decrypt_options[option] = True
        except Exception:
            pass
    
    # sets boolean value for an option
    def restore_albums():
        component_functions.invert_decrypt_option('restore_albums')

    # sets boolean value for an option
    def restore_albumnames():
        component_functions.invert_decrypt_option('restore_albumnames')

    # sets boolean value for an option
    def restore_filenames():
        component_functions.invert_decrypt_option('restore_filenames')

    # log data to a textbox in the patchbay by box name
    def append_textbox(data : (str, list), textbox_name):
        # appends to a named text box
        def logme(data, textbox_name):
            global gui_patchbay
            try:
                text_edit = gui_patchbay[textbox_name]
                current_md = text_edit.toMarkdown()
                new_md = current_md + "\n" + data
                text_edit.setMarkdown(new_md)
            except Exception as e:
                print(f'failed to append to action log, {e}')

        # both lists and strings are supported as parameters.
        if type(data) == list:
            for thing in data:
                logme(thing, textbox_name)
        else:
            logme(data, textbox_name)

    # clears data from a text box... wowsers
    def clear_textbox(textbox_name):
        global gui_patchbay
        try:
            gui_patchbay[textbox_name].clear()
        except Exception as e:
            pass

    # append to the action log
    def append_action_log(data : (str, list)):
        component_functions.append_textbox(data, 'action_log')

    # clear and add the relevant data concerning backup metadata
    def append_metadata_log(data : (str, list)):
        component_functions.clear_textbox('metalog')
        component_functions.append_textbox(data, 'metalog')

    # clears and prints metadata of a backup in the metadata box
    def display_metadata():
        global current_backup
        try:
            backup_path = current_backup['path']
            if os.path.isdir(backup_path) and backup_path != "":
                meta_display = core.backup.summary(backup_path)
                component_functions.append_metadata_log(meta_display)
                component_functions.append_action_log(f'parsed information for backup at: "...{backup_path[-20:]}"')
            else:
                component_functions.append_metadata_log('no valid backup selected...')
                component_functions.append_action_log(f'parsed information for backup at: "...{backup_path[-15:]}"')
        except Exception as e:
            component_functions.append_action_log(f'provided pathway "...{backup_path[-15:]}" too recursive, not a backup')
            component_functions.append_metadata_log('no valid backup selected...')


    def testpass():
        global current_backup, gui_patchbay
        try:
            text = gui_patchbay['password_box'].text()
            bcrypt = current_backup['bcrypt']
            if bcrypt == '':
                component_functions.append_action_log('oops, a valid backup with a "meta.json" file must be selected before testing password')
            else:
                result = pkc.check.password(text, bcrypt)
                if result:
                    component_functions.append_action_log('[CORRECT] - password matches hashed password from backup...')
                else:
                    component_functions.append_action_log('[INCORRECT] - password does not match hashed password from backup...')
        except Exception as e:
            print(e)

    
    # if called, will decrypt the currently selected backup
    def decrypt_backup():
        global decrypt_options, current_backup, gui_patchbay

        # fetch variables and button values for proper decryption
        try:
            bpath = current_backup['path']
            password = gui_patchbay['password_box'].text()
            albums = not decrypt_options['restore_albums']
            albumnames = not decrypt_options['restore_albumnames']
            filenames = not decrypt_options['restore_filenames']
        except Exception as e:
            component_functions.append_action_log('unable to find a backup pathway')
            return

        # make sure a password >6 characters was provided
        if pkc.check.password_len(password):
            pass
        else:
            component_functions.append_action_log('-=-=-=-=-=-=-=-=-')
            component_functions.append_action_log('a password is needed to decrypt a backup...')
            return

        if current_backup['path'] != "":
            pathway = fgui.choose_folder()

            if pathway == "":
                component_functions.append_action_log('the provided backup pathway will not work :/')
                return
            elif len(pathway) == 0:
                component_functions.append_action_log('the provided backup pathway will not work :/')       
            else:
                if type(pathway) == list:
                    pathway = pathway[0]

                core.backup.decrypt(current_backup['path'], 
                                    pathway,
                                    password,
                                    skip_filenames=filenames, 
                                    skip_albums=albums,
                                    skip_albumnames=albumnames,
                                    debug_mode=False,
                                    report=component_functions.append_action_log
                                    )
                component_functions.append_action_log('-=-=-=-=-=-=-=-=-')
                component_functions.append_action_log('complete...')
        else:
            component_functions.append_action_log('oops, a valid backup must be selected before decrypting')
            return

    # open the source code in the default browser
    def source_code():
        bp.util.show_url(misc.github_addr)

    # simple function to test button linking
    def nullfunc():
        print('null func triggered')


#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# CLASSES
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#


# contains all button linking configurations, centralized button attachments
class patchbay():
    # append a component to the patchbay with a reference name
    def append(component_name : (str, list), element, overwrite=True):
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

    # link all the gui buttons to appropriate functions
    def configure():
        patchbay.attach_button('choose_backup', component_functions.set_backup)
        patchbay.attach_button('test_password', component_functions.testpass)

        # checkbox linking
        patchbay.attach_checkbox("Restore Albums", component_functions.restore_albums)
        patchbay.attach_checkbox("Restore File Names", component_functions.restore_filenames)
        patchbay.attach_checkbox("Restore Album Names", component_functions.restore_albumnames)
        patchbay.attach_button('Decrypt Backup', component_functions.decrypt_backup)
        patchbay.attach_button('Guide', component_functions.nullfunc)
        patchbay.attach_button('Support', Window.open_donations)
        patchbay.attach_button('Guide', Window.open_guide)
        patchbay.attach_button('Source Code', component_functions.source_code)
        component_functions.append_metadata_log('no valid backup selected...')  # set default field



# major components of the gui
class components():
    def action_buttons(btn_stretch=True):
        global gui_patchbay
        buttons_names = ['Decrypt Backup', 'Guide', 'Source Code', 'Support']
        # 0=layout, 1=dict of buttons
        btns = gcomp.build.buttonbox(buttons_names, btn_stretch=btn_stretch)
        gui_patchbay.update(btns[1])
        return btns[0]

    def input_boxes():
        global input_names
        # create default components with constructor functions
        logo = gcomp.other.image(misc.logo_recware)
        choose_backup = gcomp.gbuttons.fixed("Select Backup (unzipped)", size=390)
        inp = gcomp.other.textbox("Backup Password", width=340)
        testpass = gcomp.gbuttons.fixed("❓", colorclass='warning', size=45) # orange test button

        # add widgets to patchbay for later connection
        patchbay.append(['choose_backup', 'test_password', 'password_box'], [choose_backup, testpass, inp])

        # put components inside boxes
        password_utils = QHBoxLayout()
        # password_utils = gcomp.build.miscbox([testpass], wid_spacing=0, alignment=Qt.AlignmentFlag.AlignLeft)
        password_utils.addWidget(testpass, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft)
        password_utils.addWidget(inp, stretch=0, alignment=Qt.AlignmentFlag.AlignLeft)


        layout = gcomp.build.miscbox([logo, choose_backup, password_utils], vertical=True, alignment=Qt.AlignmentFlag.AlignLeft)
        # layout.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        return layout

    def metadata_box():
        global gui_patchbay
        metalog = QVBoxLayout()
        label = gcomp.core.boxthis(QLabel("Backup Data"), vertical=False)
        databox = gcomp.core.term(placeholder='', maxheight=500)
        metalog.addWidget(databox)
        gui_patchbay['metalog'] = databox

        layout = QVBoxLayout()
        layout.addLayout(label)
        layout.addLayout(metalog)
        # return gcomp.build.miscbox([label, metalog], wid_spacing=0, vertical=True, alignment=Qt.AlignmentFlag.AlignHCenter)
        return layout

    # bottom box on gui for logging events of the program
    def action_log():
        global gui_patchbay
        layout = QGridLayout()
        syslog = gcomp.core.term(placeholder='', maxheight=1000)
        gui_patchbay['action_log'] = syslog
        layout.addWidget(syslog)
        return layout

    # checkboxes for toggling decryption options
    def config_boxes():
        global gui_patchbay
        layout = gcomp.build.checkbox_box(['Restore Albums', 'Restore File Names', 'Restore Album Names'])
        patchbay.append([thing for thing in layout[1].keys()], [thing for thing in layout[1].values()])
        return layout[0]

    def dono_title():
        # the title of the donation page
        misc.dono_title = "Feed a cat in need of tuna... or don't, she bites my ankles for no reason 🙃 XMR and Ko-Fi are supported!"
        cache = QLabel(misc.dono_title)
        cache.setStyleSheet(styles.color_underline())
        label = gcomp.core.boxthis(cache, vertical=False, alignment=Qt.AlignmentFlag.AlignCenter)
        return label

    def dono_kitty():
        global ms_kitty
        # kitty image :)
        kot = gcomp.other.image(misc.ms_kitty)
        kot.setStyleSheet(styles.color_box())
        logo = gcomp.build.miscbox([kot], vertical=True, wid_spacing=0, alignment=Qt.AlignmentFlag.AlignLeft)
        return logo

    # creates the text box introducing the guide (markdown formatted)
    def guide_intro():
        try:
            textbox = gcomp.core.term(placeholder='', maxheight=2000, maxwidth=10000)
            textbox.setMarkdown(misc.pk_guide_header)
            textbox.setStyleSheet(styles.color_underline())
        except Exception as e:
            print(f'::ERROR:: failed guide_intro() "{e}"')
        return textbox

    # creates the page title, guide intro, and the guid photo for reference
    def guide_header():
        cache = misc.dono_title = "Everything you need to know in order to recover your data!"
        cache = QLabel(misc.dono_title)
        cache.setStyleSheet(styles.color_underline())
        label = gcomp.core.boxthis(cache, vertical=False, alignment=Qt.AlignmentFlag.AlignCenter)

        # combine the demo image of the gui with the header and intro.
        demo = gcomp.other.image(misc.gui_demo)
        demo.setStyleSheet(styles.color_box(rad=5))
        intro = components.guide_intro()
        
        nest = gcomp.build.miscbox([intro, demo], vertical=False, stretchlist=[1, 0], alignment=Qt.AlignmentFlag.AlignRight)

        layout = gcomp.build.miscbox([label, nest], vertical=True, stretchlist=[1, 1], wid_spacing=0, alignment=Qt.AlignmentFlag.AlignCenter)
        return layout

    # the markdown boxes with instructions as well as legal bleh
    def guide_body():
        try:
            textbox = gcomp.core.term(placeholder='', maxheight=1500)
            textbox.setMarkdown(misc.pk_guide_body)
            textbox.setStyleSheet(styles.color_underline())
        except Exception as e:
            print(f'::ERROR:: failed guide_intro() "{e}"')
        return textbox


    # donation buttons used to display donation links
    def dono_options():
        # the message box on the donation page
        right = QVBoxLayout()
        m_box = gcomp.core.term(placeholder='', maxheight=9000)
        m_box.append(misc.dono_message)
        right.addWidget(m_box, stretch=1)

        # add the message and
        layout = QVBoxLayout()
        layout.addLayout(right, stretch=1)
        btn = gcomp.core.logo_term(os.path.join(misc.icon_source, 'github 75 square.png'), misc.github_addr)
        layout.addLayout(btn)
        btn = gcomp.core.logo_term(os.path.join(misc.icon_source, 'kofi_logo 75 square.png'), misc.kofi_addr)
        layout.addLayout(btn)
        btn = gcomp.core.logo_term(os.path.join(misc.icon_source, 'xmr 75 square.png'), misc.monero_addr)
        layout.addLayout(btn)
        return layout

# components combined into pages/windows 
class pages():
    # main window of the application with all components
    def default():
        global gui_patchbay
        # the top of the page including inputs, metadata, and logo
        page_top = gcomp.build.miscbox([components.input_boxes(), components.metadata_box()], stretchlist=[0, 1])

        # add the gui main groups
        layout = gcomp.build.miscbox([page_top,
                                     components.config_boxes(),
                                     components.action_buttons(),
                                     components.action_log()],
                                     vertical=True,
                                     stretchlist=[0, 0, 0, 1])
        return layout

    # support page for the application
    def donate():
        # fetch components
        title = components.dono_title()
        kot = components.dono_kitty()
        btn = components.dono_options()

        right_page = gcomp.build.miscbox([kot, btn], vertical=False, alignment=Qt.AlignmentFlag.AlignBottom)
        # build the page
        page = QVBoxLayout()
        page.addLayout(title)
        page.addLayout(right_page)
        return page

    def guide():
        header = components.guide_header()
        body = components.guide_body()
        page = gcomp.build.miscbox([header, body], vertical=True, stretchlist=[1, 1])
        return page


class Window(QWidget):
    def __init__(self):
        super().__init__()
        global syslog, gui_patchbay
        self.resize(950, 650)
        self.setWindowTitle("Photok Recware 0.2")
        layout = QVBoxLayout()
        
        # add major components
        layout.addLayout(pages.default())
        patchbay.configure()  # add all the button and widget links
        self.setLayout(layout)

    # display the donations page with my cat :))))))))))
    def open_donations():
        page = QDialog()
        page.setWindowTitle('feed my cat :)')
        page.setLayout(pages.donate())
        page.setWindowOpacity(0.9)
        page.exec()

    # display the usage guid for the program
    def open_guide():
        page = QDialog()
        page.resize(900, 600)
        page.setWindowTitle('Guide V1')
        page.setLayout(pages.guide())
        page.setWindowOpacity(0.9)
        page.exec()


#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# BUILD APPLICATION AND LAUNCH
#-=-=-==--=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

app = QApplication(sys.argv)
app_icon = QtGui.QIcon()
apply_stylesheet(app, theme='dark_teal.xml', invert_secondary=False, extra=extra)
app_icon.addFile(misc.logo_recware, QtCore.QSize(50,50))
app_icon.addFile(misc.logo_recware, QtCore.QSize(100,100))
window = Window()
window.setWindowIcon(app_icon)
window.setWindowOpacity(0.95)
window.show()
app.exec()
