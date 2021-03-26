import os
import eel

folder_global_name = ""

@eel.expose
def openLogWindow(folder_name):
    if(not os.path.isfile(f"{folder_name}/.vault.logs")):
        return False
    try:
        eel.show('logs.html')
        global folder_global_name
        folder_global_name = folder_name
        return True
    except:
        return False

@eel.expose
def get_visited_datetimes():
    if(not os.path.isfile(f"{folder_global_name}/.vault.logs")):
        return []

    with open(f"{folder_global_name}/.vault.logs", "r") as fil:
        datetime = fil.read().strip()
        datetime_split_list = datetime.split('\n')
        date_time_list = list(map(lambda x: x.split(';'), datetime_split_list))
        return date_time_list