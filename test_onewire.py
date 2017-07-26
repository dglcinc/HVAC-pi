import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.WARNING)

import HVAC.OneWire

print("Default 1-wire status = ")
print(HVAC.OneWire.status())
print("IsCelcius 1-wire status = ")
print(HVAC.OneWire.status(1))
print("IsFahr 1-wire status = ")
print(HVAC.OneWire.status(0))

'''
Requires the GPIO setup with one-wire devices attached
'''
