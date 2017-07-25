# HVAC-pi
This package is designed to control a custom HVAC system using a Raspberry Pi 3 Model B.

## Components
The package consists of the following components:

* HVAC - a Python package used to read and write the status of the HVAC system using GPIO pins on the RPi, consisting of the following modules:
	* HVAC - initially, just the status() function that returns a JSON status of the HVAC devices (relays, temp sensors, power); overall interaction with the package
	* Relay - functions associated with accessing the relays on the system.
	* Therm - functions associated with 1-wire devices attached to the HVAC system (currently just DS18B20 temperature sensors) - uses w1thermsensor library, simpler interface than the code in OneWire, which just parses the device files from the w1gpio and w1therm modules. Gives you an interface to set the precision on the therms.
	* OneWire (obsolete) - uses the device files from the one-wire GPIO/therm modbus interface to report temps for attached one-wire therms.
	* Power - a module that calls the stats.htm page for the TED5000 (mine is at 192.168.1.124, hardcoded into Relay.py) and re-formats the status into a JSON object. Currently just gets the values for the MTUs, can easily be modified to get any of the real-time values available on the stats page.
* Local (not done yet) - a local website that invokes the HVAC.status() an returns a formatted web page.
* IOT (not done yet) - a local daemon that polls HVAC.status() once a second and sends the output as an MQTT message to AWS IOT. An AWS Lambda saves off the data via SQS.

## Implementation Notes
I'm using w1thermsensor in Therm.py to implement the temp readings. It's easier than the old school reading the device files and it also gives an interface for setting the precision on the therm (transient or persistent)

My mileage with w1thermsensor: changing the precision on the therm had almost no impact on performance. It takes about one second per sensor regardless. Not sure if the overhead (above the read time spec for the sensor) is due to inefficiencies in the drivers or the python library, but it's slow. I originally wanted to do a one-second sampling for my HVAC, which would work for the other components but not for the therms. Will compromise and do a five-second sampling. This is fine for the therms, not ideal for the TED and relays. I may split out the therm updates separately so I can get one-second sample on the other two (the modular code allows this to be done easily.)

I want the Local interface (a web page you get by hitting the webserver on the Pi) to be simple, so it's going to be a Python CGI that formats a decent styled responsive page. Anything else would be ridiculous overkill. Currently I'm not planning on storing the timeseries data locally, so no need for charting (that plan may change...)

Once I get the MQTT feed set up for AWS IOT, I'll store the data in S3/Dynamo/etc. and get a little more nutty with the charting on the timeseries data.
