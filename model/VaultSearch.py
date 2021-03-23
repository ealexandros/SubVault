import glob
from pathlib import Path

import os

def get_os_system():
    if(os.name == 'nt'):
        return '\\'
    return '/'

def sub_vault_search():
    vl_files = glob.glob(os.path.abspath('*.vl'))
    if(vl_files == []):
        return None

    file_names = list(map(lambda x: x.split(get_os_system())[-1], vl_files))
    sizes = [Path(x_file).stat().st_size for x_file in file_names]
    return list(zip(file_names, sizes))

def name_vault_search(name):
    file_names = list(map(lambda x: x.split(get_os_system())[-1], glob.glob(os.path.abspath('*/'))))
    return list(filter(lambda x: name == x, file_names)) != []