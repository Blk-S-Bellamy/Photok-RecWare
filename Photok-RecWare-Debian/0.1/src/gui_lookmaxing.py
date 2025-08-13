from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

version = """
 ⠀⠀⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣻⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⠉⠳⠂⢲
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠁
⠀⠀⣿⣿⣿⣿⣿⣿⡿⣿⡽⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⢰⣿⣿⣿⡿⢷⣤⣙⣿⣿⣿⣹⣿⣿⣿⣿⢿⣿⣯⣿⣿⣿⣿⣿⣿⢤⡎⠀⠀
⣴⣿⣟⠛⠋⣢⡤⣽⣿⣿⠯⠛⠟⠛⠏⠛⠣⡿⣿⡿⣿⣿⣿⣿⣿⣿⢺⠇⠀⠀
⣿⣿⣿⡩⠽⣻⢿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣾⣿⣿⣿⣿⠸⠀⠀⠀
⣿⣿⣿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠉⠙⣿⣿⣿⣿⡆⣆⠀⠀
⣿⣿⠛⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠂⢕⣂⣤⢤⣄⠀⠈⣟⣿⣿⣿⣿⡄⠀
⢻⣿⡙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠟⠉⠁⠈⠛⢧⡠⢜⣿⣿⣿⣿⣧⠀
⢸⣿⢡⣀⡀⠀⠀⠀⠀⢀⠀⢀⣴⣿⠟⣁⠄⠂⣁⣄⠀⠀⢣⢈⢿⣿⣿⣿⡉⠀
⠀⢹⡟⠉⠛⠻⠿⣶⣄⡀⠉⢰⠞⢁⣨⠖⢿⠿⠉⠉⠁⠀⠀⣇⠘⣿⠝⣻⣇⠀
⠀⠀⣧⠀⣀⣤⣴⣴⣢⢼⠀⠀⠓⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡏⢆⠃⣿⡀
⠀⠀⣿⠐⢏⠨⠋⠁⠀⡞⡆⠀⠱⡈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⡇⠤⢠⣿⠁
⣠⣀⣿⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠱⣀⠀⠀⠀⠀⠀⠀⠀⢁⡖⠀⣿⣶⣿⠋⠀
⣿⣿⣿⣇⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⢠⡟⠀⠀⣿⣿⣿⣶⡇
⣿⣿⣿⣿⣆⠀⠀⠀⠀⠰⣳⣴⠖⢉⠭⠊⠀⠀⠀⠀⠀⠈⠀⠀⠀⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣷⣦⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠄⠀⠀⠀⠀⢰⣻⡿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣯⡢⡀⠀⢤⡐⢉⡉⢭⡤⠘⡁⡕⠀⠀⠀⢀⡞⡂⣷⡘⢿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢯⠩⠑⠀⠁⠀⣀⠄⠄⠁⠀⠀⢀⣞⠚⠀⢸⣹⡘⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠒⠒⠚⠉⠁⠀⠀⠀⠀⣠⢿⠁⠀⠀⠀⡏⡇⢩
⣿⣿⣿⣿⣿⣿⣿⣿⡿⡵⢁⢾⣄⠀⠀⠀⠀⠀⠀⠀⣰⠏⠄⠀⠀⠀⠀⠃⢠⠀
⣿⣿⣿⣿⣿⣿⢟⠟⡌⠘⢅⣾⢻⠢⢄⣀⣀⣀⡤⠞⠁⠀⠀⠀⠀⠀⠀⡄⠘⠀
>> oh yea...
"""


def about():
    print(version)


class effects():
    def shadow1():
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 160))
        return shadow


# css style sheets for the application
class styles():
    def color_box(color='teal', top=5, left=2, right=5, bottom=2, rad=25):
        css = f"""
    border-top: {top}px solid {color};
    border-left: {left}px solid {color};
    border-right: {right}px solid {color};
    border-bottom: {bottom}px solid {color};
    border-radius: {rad};
"""
        return css

    def color_underline(color='teal', bottom=3):
        css = f"""
    border-bottom: {bottom}px solid {color};
"""
        return css