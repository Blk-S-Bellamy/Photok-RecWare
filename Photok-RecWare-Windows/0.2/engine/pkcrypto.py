import hashlib
import bcrypt
from Crypto.Cipher import AES
import engine.templates as tmp

retdata = tmp.retdata
failme = tmp.failme

## SUMMARY
# ----------------
# A. All functions are pythonic representations of the Kotlin code used in Photok,
# many are unsafe by crypto security standards due to their adherance to Photok source
# code crypto methods. Primary goal is data recovery, not implementing "rolling" my own crypto.
# Primary point is, use this for recovering Photok files/backups, NOT handling your programs crypto
#
# B. 'nonce' is wrongly called 'IV' in Photok 'EncryptionManager', for the AES 256 GCM mode,
# the correct term 'nonce' will be used from now on here. This specific naming convention highlights the importance of 
# a unique and non-reused NONCE (Number ONCE).
#
# C. Photok uses AES 256 GCM mode with a non-standard (unsafe) implementation
# KEY: SHA-256 hash object (32-bytes)
# NONCE: created by turning first 16 characters of the password into bytes (16-bytes) (UNSAFE OMG PLS NO GOD HELP US ALL)
# TAG: defined as the last 16 bytes of the file, used to determine decrypt success and tampering
# file: [encrypted-filedata|16-byte-tag].photok
# 
# D. Thanks to Leon and contributors for putting out open-source software, despite the flaws, I quite
# enjoyed the application when I used it. Keep up the good work and know I hold no ill-will :)
# - BKS Bellamy


# contains functions for taking advantage of Photok's encryption
# not currently complete, still chaining vectors for an effective one-click attack :3
class hack():
    # xor two binary files to extract information
    def xor(filedata1, filedata2):
        return bytes(x ^ y for x, y in zip(filedata1, filedata2))


# used to check validity of results in keys and file operations
class check():
    # checks the GCM cryptographic tag to ensure that a file was correctly decrypted and isn't tampered with
    def tag(cipher : object, tag : bytes):
        global retdata
        ret = retdata
        ret['errors'] = []

        try:
            ret['failed'] = cipher.verify(tag)
            ret['data'] = "passed GCM tag auth..."
            return ret
        except ValueError as e:
            return failme("failed decryption or was tampered with...")

    # check the password against the bcrypt hash to see if credentials are correct
    def password(password : str, bcrypthash : str):
        global retdata
        ret = retdata
        checkme = password.encode('utf-8')
        bcrypthash = bcrypthash.encode('utf-8')
        return bcrypt.checkpw(checkme, bcrypthash)

    def password_len(password : str):
        try:
            if len(password) >= 6:
                return True
        except Exception:
            pass
        return False


class generate():
    # highly dangerous method of creating a nonce, not random, and identical between
    # files. Only used because Photok is hard coded in this manner.
    def nonce(password: str) -> bytes:
        global retdata
        ret = retdata

        try:
            # Take the first 16 characters of the password
            first_chars = password[:16]
            # Convert each character to a byte by taking its ASCII (or Unicode) code & truncating to 1 byte
            # This mimics Kotlin's .toByte() which takes the lower 8 bits of the char code
            nonce_bytes = bytes([ord(c) & 0xFF for c in first_chars])
            # If password is shorter than 16 chars, pad the IV with zeros
            nonce = nonce_bytes.ljust(16, b'\x00')
            ret['data'] = nonce

            return ret
        except Exception as e:
            return failme(e)


    # generate key using the same checks as photok
    def key(password : str):
        global retdata
        ret = retdata

        # check password character length and encode
        try:
            if len(password) >= 6:
                key = hashlib.sha256(password.encode('utf-8')).digest()
                ret['data'] = key
                return ret
            else:
                return failme(f"password is too short, {len(password)}\\6 characters")
        except Exception as e:
            return failme(e)


# decrypts filedata in a non-streamed manner (for small files)
def decrypt(filedata, password):
    global retdata
    ret = retdata

    nonce = generate.nonce(password)['data']
    key = generate.key(password)['data']  # 16-bytes, this is non-standard but Photok defined
    tag = filedata[-16:]  # used to verify data validity
    cryptdata = filedata[:-16]

    # decrypt the data using the key and gcm mode
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    rawdata = cipher.decrypt(cryptdata)

    # verification step used by higher level functions
    data = check.tag(cipher, tag)
    ret['failed'] = data['failed']
    ret['errors'].append(data['errors'])
    ret['data'] = rawdata
    return ret


# adding fully later, highly dependent on Photok procedures
"""
# decrypts files as a stream instead of loading file into memory
def decrypt_stream(filepathway, destpathway, password):
    chunk_size = 64 * 1024  # 64 KB
    with open("filepathway", "rb") as f_in, open("destpathway", "wb") as f_out:
        while chunk := f_in.read(chunk_size):
            # process chunk if needed
            f_out.write(chunk)
"""
