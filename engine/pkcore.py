import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
import pkcrypto as cx 
import pkboilerplate as boiler
import humanize
import templates as tmp
import json

retdata = tmp.retdata
failme = tmp.failme
util = boiler.util


# decryption functions for data
class cypherfile():
    # primary decryption function for individual files
    def decrypt(filepath, password, dest):
        global retdata
        ret = retdata
        
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
        except Exception as e:
            return failme(f'unable to decrypt file {e}')
            
        rawdata = cx.decrypt(file_data, password)
        with open(dest, 'wb') as fh:
            fh.write(rawdata['data'])
        
        ret['data'] = f'wrote {dest}...'
        return ret


# tools for interracting with backups
class backup():
    # load the metadata into memory from the meta.json file
    def load_meta(filepath):
        backup_metadata = {}

        # reduce repetative code and allow partial backup recovery
        def extractdata(backup_dict, category, key, value):
            try:
                # turns badly formatted JSON into an easily searchable dictionary object
                category_dict = {}
                for data in backup_dict[category]:
                    category_dict[data[key]] = data[value]
                return category_dict
            # default to assuming data is missing or broken
            except Exception as e:
                print(e)
                return {}

        try:
            with open(filepath, 'r') as fh:
                index = json.load(fh)
            # make album names searchable by uuid
            backup_metadata['albums'] = extractdata(index, 'albums', 'uuid', 'name')
            # make image album locations searchable by uuid
            backup_metadata['album_references'] = extractdata(index, 'albumPhotoRefs', 'photoUUID', 'albumUUID')
            # puts images in searchable dict to improve O factor
            backup_metadata['photos'] = extractdata(index, 'photos', 'uuid', 'fileName')
            backup_metadata['types'] = extractdata(index, 'photos', 'uuid', 'type')
            # extract additional data
            backup_metadata['created_at'] = index['createdAt']
            backup_metadata['backup_version'] = index['backupVersion']
            backup_metadata['password'] = index['password']
            return backup_metadata
        except Exception as e:
            return {}
    
    # return the summary of dir contents as well as check metadata integrity
    def summary(dirpath):
        data = []
        skip = [".tn", ".vp", ".json"]

        data.append(f'## BACKUP: [...]{dirpath[-20:]}')
        data.append('### METADATA')
        data.append("---")
        # check for metadata in the archive
        metadata = backup.load_meta(os.path.join(dirpath, 'meta.json'))
        files = os.listdir(dirpath)

        # append metadata
        try:
            if metadata == {}:
                data.append('> missing metadata file \"meta.json\"')
            else:
                data.append(f'- **BCRYPT HASH:** {metadata["password"]}')
                data.append(f'- **FILES:** {len(metadata["photos"])}')
                data.append(f'- **ALBUMS:** {len(metadata["albums"])}')
                data.append(f'- **TIMESTAMP:** {metadata["created_at"]}')
        except Exception as e:
            data.append('> metadata is broken or missing components')

        # get list on non-thumbnail encrypted files
        data.append('')
        data.append('### DIRECTORY CONTENTS')
        cryptlen = 0
        thumbnails = 0
        for thing in files:
            try:
                uuid, ext = os.path.splitext(thing)
                if ext in skip and ext != ".json":
                    thumbnails += 1
                elif ext != ".json":
                    cryptlen += 1
            except Exception as e:
                pass
        # append all of the data about the folder contents to the retdata
        data.append(f'- **FILES:** {cryptlen}')
        data.append(f'- **THUMBNAILS:** {thumbnails}')
        data.append(f'- **SIZE:** {humanize.naturalsize(boiler.util.get_directory_size(dirpath))}')
        return data

    # check the password against the bcrypt hash found in the backup metadata
    # not efficient for cracking/extreme iteration. use for simple guesses
    def check_password(backup_pathway, password : str):
        backup_meta = os.path.join(backup_pathway, "meta.json")
        bhash = backup.load_meta(backup_meta)['password']
        if bhash != None:
            return {'correct' : cx.check.password(password, bhash), 'failed' : False, 'errors' : []}
        else:
            print("no password in backup")
            return {'correct' : False, 'failed' : True, 'errors' : ['no metadata password could be found']}

    # decrypts a backup, using any available archive information and skipping metadata if missing
    # point towards unzipped backup directory
    # check password before using
    def decrypt(backup_path : str, 
                destination : str,
                password : str, 
                skip_filenames=False, 
                skip_albums=False,
                debug_mode=False,
                skip_albumnames=False,
                report=None
                ):

        global retdata
        notes = ["thumbnails are useless and therefore skipped"]
        ret = retdata
        backup_meta = os.path.join(backup_path, "meta.json")  # anticipated metadata file name and location
        skip = [".tn", ".vp", ".json"]  # skip thumbnail files and the config for decryption
        # if True, skip the next file and reset to False
        passfile = False

        # feedback for decryption success
        failed = False
        decrypted = 0
        skipped = 0
        directories = 0
        errors = []

        # check for needed pathways and metadata json file
        try:
            notes.append(util.touch(backup_meta))  # make sure a meta.json file is there even if empty
            os.makedirs(destination, exist_ok=True)
            if os.path.isdir(backup_path):
                bdata = backup.load_meta(backup_meta)
                bhash, photos, albums, types, album_references = bdata['password'], bdata['photos'], bdata['albums'], bdata['types'], bdata['album_references']
            else: 
                pass
        except Exception as e:
            bhash, photos, albums, types, album_references = "", {}, {}, {}, {}
            report('metadata file was missing... files were still decrypted without names and albums')

        # iterate the directory and decrypt contents
        dirlist = os.listdir(backup_path)
        for count, file in enumerate(dirlist):
            try:
                uuid, ext = os.path.splitext(file)
            except Exception:
                # will skip this later on if getting file data errors by adding skip char
                passfile = True

            # combine meta data and crypto to extract the whole bakup
            if not ext in skip and passfile is False:
                # pathways
                target = os.path.join(backup_path, file)
                if skip_albumnames is True:
                    folder = util.albumcheck(album_references, {}, uuid, skip=skip_albums)
                else:
                    folder = util.albumcheck(album_references, albums, uuid, skip=skip_albums)
                os.makedirs(os.path.join(destination, folder), exist_ok=True)

                # checks, variables then decrypts
                name = util.namecheck(photos, uuid, types, skip=skip_filenames)

                newfile = os.path.join(destination, folder, name)
                res = cypherfile.decrypt(target, password, newfile)
                # inform if a password was wrong on one or more files
                if res['failed']:
                    failed = True
                    errors.append(f'failed to decrypt {target}, {res["errors"][0]}')
                    if report != None:
                        try:
                            report(f'-=-=-=-=-=-=-=-=-')
                            report(f'failed to decrypt {target}, {res["errors"][0]}')
                        except Exception:
                            pass
                else:
                    if report != None:
                        try:
                            report(f'-=-=-=-=-=-=-=-=-')
                            report(f'[{count} | decrypted...] \"{file}\" ')
                        except Exception:
                            pass


                print(f'[{count} | decrypted...] \"{file}\" ')
                decrypted += 1
            else:
                # skip if the file is a thumbnail
                print(f'[{count} | skipped thumbnail...] \"{file}\"')
                skipped += 1
                passfile = False

        directories = len(os.listdir(destination))
        # will print relevant data if set to debug
        if debug_mode: 
            print(f"Complete! | {directories} albums | {decrypted} files | {skipped} skipped thumbnails")
            for item in notes:
                print(f"-> {item}")
        else:
            pass
        result = {'decrypted' : decrypted, 'skipped' : skipped, 'directories' : directories}
        return {'failed' : failed, 'errors' : errors, "data" : result}
        