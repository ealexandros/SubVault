import glob
import os
import json
import base64

import errno
import pickle

NAME = "vault.vl"

def encode_folder():
    structure = []
    for path in glob.glob(os.path.abspath('vault/**/*'), recursive=True):
        relative_path = path.replace(os.getcwd(), '')
        if(os.path.isfile(path)):
            with open(path, 'rb') as fil:
                structure.append([relative_path[1:], fil.read().decode('utf-8')])
    structure_json = json.dumps(structure)
    encode_structure = base64.b64encode(structure_json.encode("utf-8"))

    with open(NAME, 'wb') as fil:
        pickle.dump(encode_structure, fil)

def check_for_sub_directory(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

def decode_folder():
    with open(NAME, 'rb') as fil:
        data = pickle.load(fil)

    decoded_structure = base64.b64decode(data)
    structure = json.loads(decoded_structure)
    for list_file in structure:
        check_for_sub_directory(list_file[0])

        with open(list_file[0], 'wb') as fil:
            fil.write(str.encode(list_file[1]))

decode_folder()