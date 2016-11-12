import requests, pickle, os, datetime
from bs4 import BeautifulSoup
from emailer import *
from config import router_username, router_pass

def create_config():
    pass


def get_connected_devices():
    url = "http://"+router_username+":"+router_pass+"@192.168.1.1/DEV_device2.htm"
    end_url = "http://192.168.1.1/DEV_device2.htm"
    headers = {'Origin': 'http://192.168.1.1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8', 'Upgrade-Insecure-Requests':'1', 'Authorization':'Basic YWRtaW46YXNha3VyYQ==', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36', 'Cache-Control': 'max-age=0', 'Referer': end_url, 'Connection': 'keep-alive'}

    r = requests.get(url, data='', headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    _wired_list = [x.text.split('\n') for x in soup.findAll('tr', {'name': 'row_rules_wired'})]
    _wired_list = [y[1:] for y in _wired_list]
    _2g_list = [x.text.split('\n') for x in soup.findAll('tr', {'name': 'row_rules_wireless_2g'})]
    del _2g_list[0][1]
    _5g_list = [x.text.split('\n') for x in soup.findAll('tr', {'name': 'row_rules_wireless_5g'})]
    del _5g_list[0][1]

    prev_wired_list = []
    prev_2g_list = []
    prev_5g_list = []
    if os.path.exists('_wired_list'):
        with open('_wired_list') as f: prev_wired_list = pickle.load(f)
    if os.path.exists('_2g_list'):
        with open('_2g_list') as f: prev_2g_list = pickle.load(f)
    if os.path.exists('_5g_list'):
        with open('_5g_list') as f: prev_5g_list = pickle.load(f)

    disconnected_wired_devices = [x for x in prev_wired_list if x not in _wired_list]
    connected_wired_devices = [x for x in _wired_list if x not in prev_wired_list]

    disconnected_2g_devices = [x for x in prev_2g_list if x not in _2g_list]
    connected_2g_devices = [x for x in _2g_list if x not in prev_2g_list]

    disconnected_5g_devices = [x for x in prev_5g_list if x not in _5g_list]
    connected_5g_devices = [x for x in _5g_list if x not in prev_5g_list]

    total_connected = connected_wired_devices+connected_2g_devices+connected_5g_devices
    total_disconnected = disconnected_wired_devices+disconnected_2g_devices+disconnected_5g_devices

    connected_obj = dict([device[2], device[3]+' : '+device[4]] for device in total_connected)
    disconnected_obj = dict([device[2], device[3]+' : '+device[4]] for device in total_disconnected)

    for ip, details in connected_obj.items():
        send_email("vgooljar@gmail.com", "R7000 ALERT: Connected Device", ip+' : '+details+'\n'+str(datetime.datetime.now()), '')
    for ip, details in disconnected_obj.items():
        send_email("vgooljar@gmail.com", "R7000 ALERT: Disconnected Device", ip+' : '+details+'\n'+str(datetime.datetime.now()), '')

    with open("_wired_list", 'wb') as f: pickle.dump(_wired_list, f)
    with open("_2g_list", 'wb') as f: pickle.dump(_2g_list, f)
    with open("_5g_list", 'wb') as f: pickle.dump(_5g_list, f)

get_connected_devices()