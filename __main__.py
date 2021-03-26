import eel
import socket

from model.VaultEditor import *
from model.VaultDiscovery import *
from model.TimeVisit import *

IPaddress = socket.gethostbyname(socket.gethostname())
if(IPaddress == '127.0.0.1'):
    exit('No internet connection.')

eel.init('view')
eel.start('index.html', size=(600, 450))