import logging
import sys
import argparse
import json
import socket
import time
import pytemperature as pt


# handle arguments
parser = argparse.ArgumentParser(description="Emit SignalK deltas for sensors and specialize data sources connected to a Raspberry Pi\n  1Wire: uses GPIO pin 4 (board pin 7) for data, with 4.7k ohm pullup to 3.3V\n  GPIO-IN: configures designated pins as INPUT_PULLUP\n  TED5000: scrapes real-time KWh usage from TED5000 MTUs\n  RedLink: scrapes thermostat info from designated mytotalconnectcomfort.com website and location", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("stype", choices=["1Wire","GPIO", "TED5000", "RedLink"], help="Specify source of sensors to emit from")
parser.add_argument("lmode", nargs="?", choices=["DEBUG", "WARNING", "INFO"], default="WARNING", help="set logger debug level")
parser.add_argument("--daemon", action="store_true", default=False,  help="run forever in a while loop")
args = parser.parse_args()

'''
if args.daemon == True:
    from logging import config
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(module)s P%(process)d T%(thread)d %(message)s'
                },
            },
        'handlers': {
            'sys-logger6': {
                'class': 'logging.handlers.SysLogHandler',
                'address': '/dev/log',
                'facility': "local6",
                'formatter': 'verbose',
                },
            },
        'loggers': {
            '': {
                'handlers': ['sys-logger6'],
                'level': args.lmode,
                'propagate': True,
                },
            }
        }
    
    config.dictConfig(LOGGING)
else:
'''
logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=args.lmode)

logger = logging.getLogger(__name__)

logging.debug(args)

while 1:
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

    if args.stype == "1Wire":
        import HVAC.Therm
        data = HVAC.Therm.status(HVAC.Therm.DEG_KELVIN)
        logger.debug(str(data))

        for d in data:
            logger.debug("value = %s" % str(d))
            if d == "AMB":
                deltas["updates"][0]["values"].append({
                    "path":  "environment.outside.thermostat.temperature",
                    "value": data[d]
                })
            else:
                deltas["updates"][0]["values"].append({
                    "path":  "environment.inside.hvac.temperature.%s" % d,
                    "value": data[d]
                })

    elif args.stype == "GPIO":
        import HVAC.Relay
        data = HVAC.Relay.status()
        logger.debug(str(data))

        for d in data:
            logger.debug("value = %s" % str(d))
            deltas["updates"][0]["values"].append({
                "path": "electrical.switch.utility.%s.state" % d,
                "value": data[d]
            })

    elif args.stype == "TED5000":
        import HVAC.TED5000
        data = HVAC.TED5000.status()
        logger.debug(str(data))

        for d in data:
            deltas["updates"][0]["values"].append({
                "path": "electrical.ac.ted5000.%s.power" % d,
                "value": data[d]
            })

    elif args.stype == "RedLink":
        import HVAC.Stats
        data = HVAC.Stats.status()
#        logger.debug(str(data))

        deltas["updates"][0]["values"].append({
            "path": "environment.outside.thermostat.humidity",
            "value": data["outhum"]
        })
        for d in data:
            if d == "outhum":
                continue
            deltas["updates"][0]["values"].append({
                "path": "environment.inside.thermostat.%s.temperature" % data[d]["name"],
                "value": pt.f2k(int(data[d]["temp"]))
            })
            deltas["updates"][0]["values"].append({
                "path": "environment.inside.thermostat.%s.humidity" % data[d]["name"],
                "value": int(data[d]["hum"])
            })
            deltas["updates"][0]["values"].append({
                "path": "environment.inside.thermostat.%s.redlinkid" % data[d]["name"],
                "value": d
            })
            deltas["updates"][0]["values"].append({
                "path": "environment.inside.thermostat.%s.state" % data[d]["name"],
                "value": data[d]["status"]
            })

    # output deltas and decide whether to continue looping
    #logger.debug("Daemon mode = %i" % args.daemon)
    if args.daemon == True:
        print(json.dumps(deltas))
        sys.stdout.flush()
        sleepytime = 0.5
        if args.stype == "RedLink":
            sleepytime = 2.0
        time.sleep(sleepytime)
    else:
        print(json.dumps(deltas,indent=2))
        sys.exit()
