import requests
import logging
from bs4 import BeautifulSoup
import re

MTU1 = "MTU1"
MTU2 = "MTU2"
MTU3 = "MTU3"
MTU4 = "MTU4"

logger = logging.getLogger(__name__)

def status():
    result = {
        MTU1:0,
        MTU2:0,
        MTU3:0,
        MTU4:0
    }
    try:
        logger.debug("Parsing TED data...")
        page = requests.get("http://192.168.1.124/api/LiveData.xml")
#        logger.debug("Page = %s" % page.text)
        soup = BeautifulSoup(page.text,"xml")

        for i in result:
#            logger.debug("I = %s" % i)
            ttag = soup.LiveData.Power.find(i).PowerNow
            result[i] = int(ttag.text)
        logger.debug("result = %s" % result)
    except:
        logger.exception("Exception collecting data from TED5000")

    return result

if __name__ == "__main__":
    logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level="DEBUG")

    status()
