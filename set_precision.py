from w1thermsensor import W1ThermSensor

for sensor in W1ThermSensor.get_available_sensors():
    print("Setting precision for: " + sensor.id)
    sensor.set_precision(9,True)
