import glob
import os
import json
import base64
import random

import errno
import pickle

import shutil

import hashlib
from Crypto.Cipher import AES

class FolderEditor:
    def __init__(self, name="vault"):
        self.NAME = name

        self.IV_SIZE = 16
        self.KEY_SIZE = 32
        self.salt = b''

    def encrypt(self, password):
        if(not os.path.isdir(self.NAME)):
            raise Exception(f'There is no folder with the name, {self.NAME}')

        structure = []
        for path in glob.glob(os.path.abspath(f'{self.NAME}/**/*'), recursive=True):
            relative_path = path.replace(os.getcwd(), '')
            if(os.path.isfile(path)):
                with open(path, 'rb') as fil:
                    structure.append([relative_path[1:], fil.read().decode('utf-8')])
        structure_json = json.dumps(structure)
        encode_structure = base64.b64encode(structure_json.encode("utf-8"))

        derived = hashlib.pbkdf2_hmac('sha256', bytes(password, encoding='utf8'), self.salt, 100000, dklen=self.IV_SIZE + self.KEY_SIZE)
        iv = derived[0:self.IV_SIZE]
        key = derived[self.IV_SIZE:]
        encrypted_structure = AES.new(key, AES.MODE_CFB, iv).encrypt(encode_structure)

        with open(f"{self.NAME}.vl", 'wb') as fil:
            pickle.dump(encrypted_structure, fil)

    def decrypt(self, password):
        with open(f"{self.NAME}.vl", 'rb') as fil:
            data = pickle.load(fil)

        derived = hashlib.pbkdf2_hmac('sha256', bytes(password, encoding='utf8'), self.salt, 100000, dklen=self.IV_SIZE + self.KEY_SIZE)
        iv = derived[0:self.IV_SIZE]
        key = derived[self.IV_SIZE:]
        decrypted_structure = AES.new(key, AES.MODE_CFB, iv).decrypt(data)

        decoded_structure = base64.b64decode(decrypted_structure)
        structure = json.loads(decoded_structure)

        if(not isinstance(structure, list)):
            return False

        for path, content in structure:
            self.check_for_sub_directory(path)
            with open(path, 'wb') as fil:
                fil.write(str.encode(content))

        return True

    def check_for_sub_directory(self, filename):
        if(not os.path.exists(os.path.dirname(filename))):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if(exc.errno != errno.EEXIST):
                    return True