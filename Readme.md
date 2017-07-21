# HVAC-pi
This package is designed to control a custom HVAC system using a Raspberry Pi 3 Model B.

## Components
The package consists of the following components:

* HVAC - a Python package used to read and write the status of the HVAC system using GPIO pins on the RPi, consisting of the following modules:
	* HVAC - initially, just the status() function that returns a JSON status of the HVAC devices (relays, temp sensors, power); overall interaction with the package
	* Relay - functions associated with accessing the relays on the system.
	* OneWire - functions associated with 1-wire devices attached to the HVAC system (currently just DS18B20 temperature sensors)
	* Power - a module that calls the stats.htm page for the TED5000 and re-formats the status into a JSON object
* Local - a local website that invokes the HVAC.status() an returns a formatted web page
* IOT - a local daemon that polls HVAC.status() once a second and sends the output as an MQTT message to AWS IOT. An AWS Lambda saves off the data via SQS.