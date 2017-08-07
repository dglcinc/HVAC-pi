import json
import os
import sys
import time
import traceback
import logging
import boto3
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

def write_status(event, context):
#    dlevel = logging.DEBUG
#    logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=dlevel)
    logger.debug("Event = " + str(event["state"]["reported"]))

    data = event["state"]["reported"]
    try:
        configPath = os.environ['LAMBDA_TASK_ROOT'] + "/hvac.html"
        logger.debug("Looking for hvac.html at " + configPath)
        configContents = open(configPath).read()
        logger.debug("HTML = " + configContents)
    except:
        logger.debug("error opening html file")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1)
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2)


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
    
    result = "Content-type: text/html\n\n"

    try:
        f = open("hvac.html","r")
        soup = BeautifulSoup(f, "html.parser")
    except IOError:
        throw("file error")

    logger.debug("Making soup...")

    for e in soup.find_all("th"):
        if e["id"] == "date":
            logger.debug("Timestamp = " + str(data["Timestamp"]))
            os.environ['TZ'] = 'US/Eastern'
            time.tzset()
            e.string = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(int(data["Timestamp"])))
    for e in soup.find_all("td"):
        logger.debug("Tag: " + str(e))
        logger.debug("Class: " + str(e["class"]))
        try:
            if e["class"] == ["rly"]:
                logger.debug("Relay item" + str(e["class"]))
                if data["Relay"][e["id"]] == True:
                    e["style"] = "background-color:green;color:black"
            if e["class"] == ["temp"]:
                e.string = "%s %d" % (e.string, int(data["Therm"][e["id"]]))
            if e["class"] == ["mtu"]:
                e.string = "%0.3f KWh" % (data["Power"][e["id"]]/1000.0)
        except:
            logger.exception("Ignoring exception")
    
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
    
    result += (soup.prettify())

    try:
        s3 = boto3.resource("s3")
        object = s3.Object("hvac.dgl.guru", "hvac.html")
        retval = object.put(
            ACL="public-read",
            Body=result,
            StorageClass="REDUCED_REDUNDANCY",
            CacheControl="no-cache",
            ContentType="text/html"
        )
        object = s3.Object("hvac.dgl.guru", "style.css")
        stylePath = os.environ['LAMBDA_TASK_ROOT'] + "/style.css"
        retval = object.put(
            ACL="public-read",
            Body=open(stylePath,"r").read(),
            StorageClass="REDUCED_REDUNDANCY",
            CacheControl="no-cache",
            ContentType="text/html"
        )
        logger.debug("Retval = " + str(retval))
    except ClientError as e:
        logger.error("Received error: %s", e, exc_info=True)

    return {
        "message": "Updated the status page",
        "event": event
    }
