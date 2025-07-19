# the land of the boring functions that simply add clutter to top level functions AND do not apply to cryptography
import magic
import webbrowser
import os


class util():
    def type_resolver(filepath):
        try:
            with open(filepath, "rb") as f:
                file_bytes = f.read()
            mime = magic.from_buffer(file_bytes, mime=True)
            return mime
        # return nothing if it is impossible to resolve filetype
        except Exception as e:
            return ''

    # return the correct folder for a given file or put in unsorted
    def albumcheck(album_references : dict, albums : dict, uuid : str, skip=False):
        try:
            # put in unsorted if no albums is requested
            if skip:
                return 'unsorted'
            else:
                album_uuid = album_references[uuid]
                try:
                    album_name = albums[album_uuid]
                # put in album uuid-named album if the actual name is missing or corrupted in the backup metadata
                except Exception:
                    return album_uuid

                return album_name  # return the album
        except Exception:
            return "unsorted"

    # fetch album default to 'unsorted' album or skip
    def namecheck(photos : dict, uuid : str, filetypes : dict, filepath="", skip=False):
        try:
            # keep uuid as name if requested with filetype as listed in backup metadata
            if skip:
                return f"{uuid}.{filetypes[uuid]}"
            else:
                return photos[uuid]
        # use mimetypes to assume the filetype if no backup metadata is found
        except Exception:
            return uuid

    # create a file if it doesn't exist
    def touch(pathway):
        try:
            with open(pathway, 'x') as f:
                # File created successfully
                print("meta.json was missing, no metadata mode...")
                return "metadata file was missing... files were still decrypted without names and albums"
        except FileExistsError:
            print("meta.json exists...")
            return "metadata file was used for decryption..."
        except FileNotFoundError:
            return 'unable to find archive'
    
    def show_url(webpage):
        webbrowser.open(webpage)

    def get_directory_size(directory):
        total_size = 0
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    total_size += entry.stat().st_size  # size of file in bytes
                elif entry.is_dir():
                    total_size += util.get_directory_size(entry.path)  # recursive call for subdirectory
        except (FileNotFoundError, PermissionError):
            pass  # ignore folders/files that can't be accessed
        return total_size