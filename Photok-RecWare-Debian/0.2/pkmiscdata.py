# misc variables that can be changed on later updates. keep logic apart from custom params
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))
dono_message = """Hey, I made this tool after having to recover some of my photos that could not be recovered using Photok. It sucks to lose anything personal and photos/videos especially! I hope that you are able to recover all of your important personal data and if you find a bug that prevents recovery, let me know on my github! I always appreciate any feedback, positive or negative as it leads to my own improvement. This was a quick GUI project built on a simple module I made for decrypting my own photos from a partially broken Photok Backup. Feel free to use it as you like and even change the gui :)"""
monero_addr = '87Fc45hdTL6SSZ3ZrDGptrAPZWLs57Yo5j4kvCFp3mtm4kF6KTaLwycbApWgyj1mrTFoKFq49G9A1ftFAFrFvbaiQJbmp98'
kofi_addr = 'https://ko-fi.com/bksbellamy'
github_addr = "https://github.com/Blk-S-Bellamy/RecWare-Photok"

# pathways (logos)
logo_recware = os.path.join(absolute_path, "icons", "Photok RecWare 100.png")
ms_kitty = os.path.join(absolute_path, "icons", "feedme 250 tall.png")
logo_github = os.path.join(absolute_path, "icons", "github 75 square.png")
gui_demo = os.path.join(absolute_path, "icons", "demo half.png")
icon_source = os.path.join(absolute_path, "icons")
pk_guide_header = """
### GUIDE
- This will be fast, both backup folders and encrypted files are supported as well! Even if the metadata (information file about encrypted files) is gone, the files can still be recovered, restoring even their filetypes (.jpg, .png, .webm, etc.). I reverse engineered the encryption so you don't have to! Good luck :3
"""

pk_guide_body = """
## Restoring Backups
- Data recovery is easy to complete with only a few clicks! Keep in mind that even a broken archive can be restore without a metadata _(meta.json)_ file in it. In order, backups can be restored by:
1. **(button 1)** select the uncompressed backup folder, it cannot be zipped for this step. All information about the backup will appear in **(box 6)**
2. **(box 2)** type in the password for the backup, 
3. **(optional | button 3)** if you are not sure of the password, press to test the password. This only works if you had an intact 'meta.json' file in the backup.
4. **(optional | checkboxes 7)** if you want to change if the filenames are restored, album names, or disable sorting into the original folders, simply disable the appropriate checkbox.
5. **(button 4)** press to choose a destination folder to decrypt your files! watch **(box 5)** for if the backup was successful or not :)
## Restoring Individual Files
- a file or files encrypted with Photok but without any backup data can still be decrypted with no problem! The steps are very similar to backups:
1. **(button 1)** select a folder with encrypted files, it cannot be zipped. no backup information will appear as there is no metadata file.
2. **(box 2)** type the password into the box. **(button 3)** only works if a backup is present to test the password.
3. **(button 4)** press to attempt a decryption. Failure will say as such and the files will be still binary blobs :\ failure would be caused by files encrypted without Photok, a bad password, or Photok changing encryption scheme in the future.

### NOTE:
**Hey**, Bellamy here. I just wanted to say I am in no way connected or associated with Photok or Leon Latsch. This is just a project I made to help people recover files lose in a backup, much like I dealt with. All code is open source and provided as-is with no guarantees as laid out in the license found in the source folder. That out of the way, thanks for using and I am always available to help on my github (support button) if your backup fails for any reason!
"""