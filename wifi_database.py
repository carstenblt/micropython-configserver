import network
import time

active_wifi = None
database_file = "wifi-database"

def get_wifi(essid):
    try:
        myfile = open(database_file, "r")
    except OSError:
        return None

    line = myfile.readline()
    password = None
    while line != '':
        if line.strip() == essid:
            password = myfile.readline().strip()
            break
        myfile.readline()
        line = myfile.readline()
    myfile.close()
    return password

def add_wifi(essid, password):
    try:
        myfile = open(database_file, "r+")
    except OSError:
        myfile = open(database_file, "w+")

    line = myfile.readline()
    content = None
    while line != '':
        if line.strip() == essid:
            position = myfile.tell()
            content = myfile.readlines()
            content[0] = password + '\n'
            myfile.seek(position)
            myfile.writelines(content)
            break
        myfile.readline()
        line = myfile.readline()
    if content == None:
        myfile.write(essid + '\n' + password + '\n')
    myfile.close()

def remove_wifi(essid):
    try:
        myfile = open(database_file, "r+")
    except OSError:
        return

    line = myfile.readline()
    while line != '':
        if line.strip() == essid:
            position = myfile.tell() - len(line)
            myfile.readline()
            content = myfile.readlines()
            myfile.seek(position)
            myfile.writelines(content)
            myfile.truncate()
            break
        myfile.readline()
        line = myfile.readline()
    if content == None:
        myfile.write(essid + '\n' + password + '\n')
    myfile.close()

def iter_wifis():
    try:
        myfile = open(database_file, "r")
    except OSError:
        return None

    line = myfile.readline()
    while line != '':
        yield (line.strip(), myfile.readline().strip())
        line = myfile.readline()
    myfile.close()

def connect_and_add_wifi(essid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(essid, password)
    for i in range(50):
        time.sleep_ms(100)
        if sta.isconnected():
            add_wifi(essid, password)
            active_wifi = essid
            return True
    sta.active(False)
    return False

