# Import Libraries
from w1thermsensor import W1ThermSensor
import os
import time
import logging

logger = logging.getLogger(__name__)

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

DS1 = "0516a36332ff"
DS2 = "0516a365d8ff"
DS3 = "0316a00f04ff"
DS4 = "0516a36816ff"
DS5 = "0316a015e7ff"

dnames = {
    DS1 : "IN",
    DS2 : "OUT",
    DS3 : "CRW",
    DS4 : "AMB",
    DS5 : "Unassigned"
}

# returns a JSON object containing the current values of all 28* one-wire devices on the bus

'''
uncomment this section inside result to get default 0 for unattached sensors
        dnames[DS1] : 0,
        dnames[DS2] : 0,
        dnames[DS3] : 0,
        dnames[DS4] : 0,
        dnames[DS5] : 0
'''
sensors = W1ThermSensor.get_available_sensors()
logger.debug("Available sensors: " + str(sensors))

def status(is_celsius=0):
    logger.debug("generating status")
    result = {}
    for sensor in sensors:
        temp = 0
        if is_celsius:
            thermtemp = sensor.get_temperature(W1ThermSensor.DEGREES_C)
        else:
            thermtemp = sensor.get_temperature(W1ThermSensor.DEGREES_F)
        logger.debug("Temp for: " + sensor.id + " is: " + str(thermtemp))
        try:
            name = dnames[sensor.id]
            result[name] = thermtemp
        except KeyError:
            # this will add a new member to the dict with the name of the sensor
            result[sensor.id] = thermtemp
    logger.debug(result)
    return result
