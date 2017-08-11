import logging
import sys
import argparse
import json
import socket
import time

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Emit SignalK deltas for 1-Wire thermometers attached locally on a Raspberry Pi\n  Assumes GPIO pin 4 (board pin 7) is used for data line for 1-wire\n  Must use 4.7K ohm resistor pull-up to 3.3V on data line.", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("lmode", nargs="?", choices=["DEBUG", "WARNING", "INFO"], default="WARNING", help="set logger debug level")
parser.add_argument("--daemon", action="store_true", default=False,  help="run forever in a while loop")
args = parser.parse_args()

logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=args.lmode)
logging.debug(args)

import HVAC.Therm

while 1:
    data = HVAC.Therm.status(HVAC.Therm.DEG_KELVIN)
    logger.debug(str(data))

    deltas = {
        "updates": [
            {
                "source": {
                    "label": "rpi:%s" % socket.gethostname()
                },
                "values": []
            }
        ]
    }

    for d in data:
        logger.debug("value = %s" % str(d))
        deltas["updates"][0]["values"].append({
            "path":  "environment.inside.hvac.temperature.%s" % d,
            "value": data[d]
        })
    
    logger.debug("Daemon mode = %i" % args.daemon)
    if args.daemon == True:
        print(json.dumps(deltas))
        time.sleep(0.2)
    else:
        print(json.dumps(deltas,indent=2))
        sys.exit()
