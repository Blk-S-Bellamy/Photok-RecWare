# Vault RecWare - Photok Module
![logo](https://github.com/user-attachments/assets/b0377e53-f79a-4f8b-9cfa-8f166e1f37d9)
### About
- Restore backups with broken files or missing metadata.
- Full file decryption with password only and filetype sensing for file postfixes.
- Choose to restore with or without restoring filenames, albumnames, or original albums.
- Easy to use and launch as a portable tool, no need to install.
- Open-source code is available for review, contributing, or compiling.
- Recover standalone Photok files without any provided metadata.

An open-source graphical program to enable speedy, efficient recovery of [Photok](https://github.com/leonlatsch/Photok/blob/develop/README.md) backups or standalone files. I created this over the course of a week when I found my photo backup to be non-recoverable using the Photok application when importing to my new phone.

Written in [Python](https://www.python.org/), the program is released for multiple platforms and includes source code and compile instructions for those wanting to contribute or test! Default look is dark mode and demonstrated for Windows 10/11 and Debian below:

<img width="585" height="300" alt="platform demo" src="https://github.com/user-attachments/assets/76433bf2-0a9b-4aef-bf81-8611daa35d02" />

*This program is __not__ associated with [Photok](https://github.com/leonlatsch/Photok/blob/develop/README.md) for android but serves to enable data recovery from Photok-encrypted backups and files. 0% of Photok's source code has been used and eveything has been written from the ground up in Python*

---
[![Windows 10](https://img.shields.io/badge/Windows_10-Yes-green)](https://github.com/Blk-S-Bellamy/Photok-RecWare/releases/tag/Win-0.1)
[![Windows 11](https://img.shields.io/badge/Windows_11-Yes-green)](https://github.com/Blk-S-Bellamy/Photok-RecWare/releases/tag/Win-0.1)
[![Debian](https://img.shields.io/badge/Debian-Yes-green)](https://github.com/Blk-S-Bellamy/Photok-RecWare/releases/tag/Deb-0.1)
[![Linux](https://img.shields.io/badge/Linux-Most-yellow)](https://github.com/Blk-S-Bellamy/Photok-RecWare/releases/tag/Deb-0.1)
[![Nuthin](https://img.shields.io/badge/Android-Unsupported-red)](https://github.com/Blk-S-Bellamy/Photok-RecWare/releases)
[![Nuthin](https://img.shields.io/badge/IOS-Unsupported-red)](https://github.com/Blk-S-Bellamy/Photok-RecWare/releases)

# Turn Cryptography back to to Kitties!
With only a few presses, you can decrypt only the useful files in your locked backup. By default, thumbnails are skipped, file names, and albums are restored. If you are not quite sure of your password for a backup, you can test using the orange button by the password box. Overall, the guide can tell you anything else you may have questions on. Good luck!

<img width="958" height="248" alt="crypttokitty" src="https://github.com/user-attachments/assets/fbd97b8b-7b10-41ef-a7f8-5ed028e32b3d" />

---
# Support

<a href="https://ko-fi.com/bksbellamy">
  <img src="https://github.com/user-attachments/assets/a52b3d0c-24e4-47c7-87e6-9681b4110f03" width="100" height="50" alt="Button Image" />
</a>
<a href="https://www.getmonero.org/">
  <img src="https://github.com/user-attachments/assets/a73692f2-18dd-4504-8ad0-b83bb9ff0dd3" width="100" height="50" alt="Button Image" />
</a>

```
XMR: 87Fc45hdTL6SSZ3ZrDGptrAPZWLs57Yo5j4kvCFp3mtm4kF6KTaLwycbApWgyj1mrTFoKFq49G9A1ftFAFrFvbaiQJbmp98
```

---

# Compiling From Source
The release versions of the program are single binary files containing compiled Python3 code and any media used as graphical assets. This is for portability, dependability, and due to the easy of distribution. Pyinstaller is used in order to create the application for Windows and Linux and instructions can be found in the source code folder for each release and here:

### Debian
1. Navigate to the source directory in a Bash terminal (contains gui.py)
2. Install system dependencies
```sh
# install python3, pyenv, create a venv, and activate it
sudo apt install python3
sudo apt install python3-venv
```
3. Create and activate the Python virtual environment
```sh
python3 -m venv venv
source venv/bin/activate
```
4. Install Python3 dependencies
```sh
pip install -r requirements.txt
pip install -U pyinstaller
```
5. Compile the program as a portable binary
```sh
# One binary file
pyinstaller --onefile --add-data "icons:icons" gui.py
# >>OR<<
# binary file with subdirectory of compiled scripts
pyinstaller --add-data "icons:icons" gui.py
```
- The built program will be in the 'dist' directory

### Windows 10/11
- The dependencies are different for Debian and Windows, make sure to build from Windows source code!
1. Install python3 from python.org.
2. Make sure to add Python to 'PATH' and enable longpaths too (checkboxes in python installer).
3. Navigate to the source directory in a cmd terminal (contains gui.py).
4. Create the Python3 virtual environement and activate it
```bin
python3 -m venv "path\to\folder\venv
venv/Scripts/activate.bin
```
5. Install Python3 requirements
```bin
pip install -r requirements.txt
pip install pyinstaller
```
6. Build from source
```bin
pyinstaller --onefile --noconsole --add-data "icons:icons" gui.py
# >>OR<<
# binary file with subdirectory of compiled scripts
pyinstaller--noconsole --add-data "icons:icons" gui.py
```
- The built program will be in the 'dist' directory
---
