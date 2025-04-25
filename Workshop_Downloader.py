
# Easily download items directly from the steam workshop

from urllib.parse import urlparse
from urllib.parse import parse_qs
from subprocess import run
import os

workshopIds = []
appId = 105600

# Parse list of urls to get array of ids
with open("Links.txt","r") as file:
    while True:
        l = file.readline()
        if l == "" or l == None:
            break
        q = urlparse(l).query
        i = parse_qs(q)["id"][0]
        workshopIds += [i]

# Write script file for steamcmd
with open("steamcmd.txt","w") as file:
    file.write("force_install_dir ../steam_downloads\n")
    file.write("login anonymous\n")
    for i in workshopIds:
        file.write("workshop_download_item "+str(appId)+" "+str(i)+"\n")
    file.write("quit")

# Tell steamcmd to run script
run(["steamcmd\\steamcmd.exe","+runscript","..\\steamcmd.txt"])

# Script finished
# Rename id folders to the name of the mod
for i in workshopIds:
    try:
        path = "steam_downloads\\steamapps\\workshop\\content\\"+str(appId)+"\\"+str(i)
        with open(path+"\\pack.json","r") as file:
            f = file.read()
            start = f.find("\"Name\":")+9
            end = f.find("\"",start)
            name = f[start:end]
        os.rename(path,"Downloaded Files\\"+str(name))
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        pass
