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


def status():
    result = {}

    # log in to mytotalconnectcomfort.com
    try:
        cj = cookielib.CookieJar()
        br = mechanize.Browser()
        br.set_cookiejar(cj)
        br.open("https://www.mytotalconnectcomfort.com/portal")
        br.select_form(nr=0)
        br.form['UserName'] = hs.uid
        br.form['Password'] = hs.pwd
        br.submit()
    
        stats_page = br.response().read()
        logger.debug(stats_page)
    except:    
        logger.exception("Error scraping MyTotalConnectComfort.com")
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
