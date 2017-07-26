# "pulling it all together" module
import Relay
import Power
# import OneWire
import Therm

import time
import logging
import json

#from OneWire import dnames
from Therm import dnames
from Relay import R

logger = logging.getLogger(__name__)

'''
The status() function returns JSON as follows:
{
    "HVAC-pi" : "v1.0",
    "Relay" : {
        "ZV" : "off",
        "DHW" : "off",
        "BLR" : "off",
        "RCHL" : "off",
        "LCHL" : "off",
        "Y2ON" : "off",
        "YOFF" : "off",
        "Y2FAN" : "off",
    },
    "OneWire" : {
        dnames[OneWire.DS1] : 0,
        dnames[OneWire.DS2] : 0,
        dnames[OneWire.DS3] : 0,
        dnames[OneWire.DS4] : 0
        dnames[OneWire.DS5] : 0
    },
    "Power" : {
        "MTU1_KW" : 0,
        "MTU2_KW" : 0,
        "MTU3_KW" : 0,
        "MTU4_KW" : 0
}
'''

def status():
    stat = {
        "HVAC-pi" : "v1.0",
        "Timestamp" : "",
        "Relay" : {
        },
        "Therm" : {
        },
        "Power" : {
        }
    }

    ows = Therm.status()
    logger.debug(ows)
    stat["Therm"] = ows

    pwr = Power.status()
    logger.debug(pwr)
    stat["Power"] = pwr

    rly = Relay.status()
    stat["Relay"] = rly

    stat["Timestamp"] = time.time()

    return json.dumps(stat, indent=2)
