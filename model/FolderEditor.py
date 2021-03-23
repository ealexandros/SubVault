import glob
import os
import json
import base64

import errno
import pickle

import shutil

class FolderEditor:
    def __init__(self, name="vault"):
        self.NAME = name 

    def encrypt(self):
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

        with open(f"{self.NAME}.vl", 'wb') as fil:
            pickle.dump(encode_structure, fil)

    def decrypt(self):
        with open(f"{self.NAME}.vl", 'rb') as fil:
            data = pickle.load(fil)

        decoded_structure = base64.b64decode(data)
        structure = json.loads(decoded_structure)

        for path, content in structure:
            self.check_for_sub_directory(path)
            with open(path, 'wb') as fil:
                fil.write(str.encode(content))

    def del_folder(self):
        shutil.rmtree(self.NAME)

    def check_for_sub_directory(self, filename):
        if(not os.path.exists(os.path.dirname(filename))):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if(exc.errno != errno.EEXIST):
                    raise Exception('File already exists.')