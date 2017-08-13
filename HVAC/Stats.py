import mechanize
from bs4 import BeautifulSoup
import urllib2 
import cookielib
import honeywellsecrets as hs
import time
import logging
from bs4 import BeautifulSoup
import json
import re

logger = logging.getLogger(__name__)
site_ready = False
logged_in = False
retrying = False
locationId = ""
locationId_prog = re.compile("GetZoneListData\?locationId=([0-9][0-9]*)&")

try:
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    site_ready = True

except:
    logger.exception("Error prepping Redlink scrape")

def status():
    global site_ready
    global logged_in
    global retrying
    global locationId
    global locationId_prog
    global cj, br

    result = {}

    # log in to mytotalconnectcomfort.com
    # NOTE: this code currently only works if you only have one location defined...
    if site_ready:
        try:
            if logged_in == False:
                logger.debug("Not logged in; logging in...")
                br.open("https://www.mytotalconnectcomfort.com/portal")
                br.select_form(nr=0)
                br.form['UserName'] = hs.uid
                br.form['Password'] = hs.pwd
                response = br.submit()
                stats_page = response.read()
                list = locationId_prog.findall(stats_page)
                locationId = list[0]
                logger.debug("locationId=%s" % locationId)
                logged_in = True
            else:
                refresh_link = "https://www.mytotalconnectcomfort.com/portal/%s/Zones" % locationId
                logger.debug("Refresh link = %s" % refresh_link)
                br.open(refresh_link)
#                response = br.response()
                response = br.reload()
                stats_page = response.read()
            logger.debug("Stats page = %s" % stats_page)
        except:    
            logger.exception("Error scraping MyTotalConnectComfort.com")
            logged_in = False
            if retrying == False:
                retrying = True
                result = status()
            else:
                retrying = False
            return result

    soup = BeautifulSoup(stats_page, "lxml")
    for e in soup.find_all("tr", "gray-capsule pointerCursor"):
        logger.debug(str(e))
        stat = {}
        stat["status"] = "off"
        for f in e.find_all():
            if f.has_attr("class"):
                if f["class"] == ["location-name"]:
                    stat["name"] = f.string
                if f["class"] == ["hum-num"]:
                    tstr = re.findall("[0-9]+", f.string)
                    if len(tstr) > 0:
                        stat["hum"] = int(tstr[0])
                    else:
                        stat["hum"] = 0
                if f["class"] == ["tempValue"]:
                    tstr = re.findall("[0-9]+", f.string)
                    if len(tstr) > 0:
                        stat["temp"] = int(tstr[0])
                    else:
                        stat["temp"] = 0
                if "coolIcon" in f["class"] and f["style"] == "":
                    stat["status"] = "cool"
                if "heatIcon" in f["class"] and f["style"] == "":
                    stat["status"] = "heat"
                if "fanOnIcon" in f["class"] and f["style"] == "":
                    stat["status"] = "fan"
        result[e["data-id"]] = stat
    return(result)
