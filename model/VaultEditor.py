import glob
import os
import json
import base64
import random
import eel

import errno
import pickle

import hashlib
from Crypto.Cipher import AES

IV_SIZE = 16
KEY_SIZE = 32
salt = b''

@eel.expose
def encrypt_folder(folder_name, password):
    if(not os.path.isdir(folder_name)):
        raise Exception(f'There is no folder with the name, {folder_name}')

    structure = []
    for path in glob.glob(os.path.abspath(f'{folder_name}/**/*'), recursive=True):
        relative_path = path.replace(os.getcwd(), '')
        if(os.path.isfile(path)):
            with open(path, 'rb') as fil:
                structure.append([relative_path[1:], base64.b64encode(fil.read()).decode('utf-8')])
    structure_json = json.dumps(structure)
    encode_structure = base64.b64encode(structure_json.encode("utf-8"))

    derived = hashlib.pbkdf2_hmac('sha256', bytes(password, encoding='utf8'), salt, 100000, dklen=IV_SIZE + KEY_SIZE)
    iv = derived[0:IV_SIZE]
    key = derived[IV_SIZE:]
    encrypted_structure = AES.new(key, AES.MODE_CFB, iv).encrypt(encode_structure)

    with open(f"{folder_name}.vl", 'wb') as fil:
        pickle.dump(encrypted_structure, fil)

@eel.expose
def decrypt_folder(vault_name, password):
    with open(vault_name, 'rb') as fil:
        data = pickle.load(fil)

    derived = hashlib.pbkdf2_hmac('sha256', bytes(password, encoding='utf8'), salt, 100000, dklen=IV_SIZE + KEY_SIZE)
    iv = derived[0:IV_SIZE]
    key = derived[IV_SIZE:]
    decrypted_structure = AES.new(key, AES.MODE_CFB, iv).decrypt(data)

    try:
        decoded_structure = base64.b64decode(decrypted_structure)
        structure = json.loads(decoded_structure)
    except:
        return False

    if(not isinstance(structure, list)):
        return False

    for path, content in structure:
        check_for_sub_directory(path)
        with open(path, 'wb') as fil:
            fil.write(base64.b64decode(content))

    return True

def check_for_sub_directory(filename):
    if(not os.path.exists(os.path.dirname(filename))):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if(exc.errno != errno.EEXIST):
                return True