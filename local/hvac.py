#!/usr/bin/python
import cgi
import cgitb
import os
import sys
import json
import time
import logging
import time
from bs4 import BeautifulSoup

cgitb.enable()

logger = logging.getLogger(__name__)
dlevel = logging.WARNING

if len(sys.argv) > 1:
    args = sys.argv[1:]
    logger.debug("Args = " + str(args))
    for arg in args:
        if arg == "DEBUG" or arg == "INFO" or arg == "WARNING":
            logger.debug("Setting log level to: " + sys.argv[1])
            dlevel = arg
        else:
            logger.exception("Unknown argument: " + arg)

# use warning for the library call, only use debug for this script
logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=dlevel)

def status_color(status="off"):
    result = "background-color:black"
    logger.debug("Status = " + status)
    if status == "cool":
        result = "background-color:blue"
    if status == "heat":
        result = "background-color:red"
    if status == "fan":
        result = "background-color:yellow;color:black"
    return result
            
print "Content-type: text/html\n\n"
#print "<meta http-equiv='refresh' content='2'/>"

from HVAC import hvac

used_cache = 0
try:
    f = open("/tmp/hvac_current.json", "r")
    if f:
        data = json.loads(f.read())
        f.close()
        if time.time() - data["Timestamp"] < 20:
            used_cache = 1
except:
    logger.exception("unable to read cache file")
    used_cache = 0

if used_cache == 0:
    data = json.loads(hvac.status())
    logger.warning("Cache out of date.")
logger.debug("Using cache: " + str(used_cache))
logger.debug("Data used = " + str(data))

try:
    f = open("hvac.html","r")
except IOError:
    print("file error")
    sys.exit(1)
soup = BeautifulSoup(f, "lxml")
logger.debug("Making soup...")
for e in soup.find_all("th"):
    if e["id"] == "date":
        logger.debug("Timestamp = " + str(data["Timestamp"]))
        e.string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(int(data["Timestamp"])))
        if used_cache == 0:
            e["style"] = "background-color:crimson"
for e in soup.find_all("td"):
    logger.debug("Tag: " + str(e))
    logger.debug("Class: " + str(e["class"]))
    if e["class"] == ["rly"]:
        logger.debug("Relay item" + str(e["class"]))
        if data["Relay"][e["id"]] == True:
            e["style"] = "background-color:green;color:black"
    if e["class"] == ["temp"]:
        e.string = "%s %d" % (e.string, int(data["Therm"][e["id"]]))
    if e["class"] == ["mtu"]:
        e.string = "%0.3f KWh" % (data["Power"][e["id"]]/1000.0)
sn = soup.find("tr", "statname")
st = soup.find("tr", "stattemp")
sh = soup.find("tr", "stathum")
for name, i in data["Stats"].items():
    nametag = soup.new_tag("td")
    temptag = soup.new_tag("td")
    humtag = soup.new_tag("td")

    nametag["class"] = "statname"
    nametag["colspan"] = 2
    nametag["name-id"] = name
    nametag.string = i["name"]
    sn.append(nametag)

    temptag["class"] = "stattemp"
    temptag["colspan"] = 2
    temptag["temp-id"] = name
    temptag["style"] = status_color(i["status"])
    temptag.string = str(i["temp"])
    st.append(temptag)

    humtag["class"] = "stathum"
    humtag["colspan"] = 2
    humtag["hum-id"] = name
    humtag.string = str(i["hum"]) + "%"
    sh.append(humtag)
print (soup.prettify())
