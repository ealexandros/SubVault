import eel

from model.FolderEditor import FolderEditor
from model.VaultSearch import *

@eel.expose
def sub_vault_search_proxy():
    return sub_vault_search()