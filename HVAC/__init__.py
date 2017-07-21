# init.py
import Relay
import Power
import OneWire

import json

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
        "Y2FAN" : "off",
    },
    "OneWire" : {
        "HDR_IN" : 0,
        "HDR_OUT" : 0,
        "CRW" : 0,
        "AMB" : 0
    },
    "Power" : {
        "MTU1_KW" : 0,
        "MTU2_KW" : 0,
        "MTU3_KW" : 0
}
'''
def status():
    stat = {
        "HVAC-pi" : "v1.0",
        "Relay" : {
            "ZV" : "off",
            "DHW" : "off",
            "BLR" : "off",
            "RCHL" : "off",
            "LCHL" : "off",
            "Y2ON" : "off",
            "Y2FAN" : "off",
        },
        "OneWire" : {
            "HDR_IN" : 0,
            "HDR_OUT" : 0,
            "CRW" : 0,
            "AMB" : 0
        },
        "Power" : {
            "MTU1_KW" : 0,
            "MTU2_KW" : 0,
            "MTU3_KW" : 0
        }
    }
    return json.dumps(stat)
