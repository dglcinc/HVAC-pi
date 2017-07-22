import HVAC

print("Default 1-wire status = " + OneWire.status())
print("IsCelcius 1-wire status = " + OneWire.status(1))
print("IsFahr 1-wire status = " + OneWire.status(0))

'''
Requires the GPIO setup with one-wire devices attached
'''