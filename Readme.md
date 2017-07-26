# HVAC-pi
This package is designed to monitor (and potentially control) a custom HVAC system using a Raspberry Pi 3 Model B. It gives me a view into the critical operating elements of the system, so I know if it is working properly. Although it is technically possible to also control the system from the Pi, I've resisted doing this because then it is very hard to get HVAC techs to work on it (or if they do they have no clue what to do.) Hence all the main operating interfaces are standard components, the Pi is just used for monitoring. At some point I may use the Pi for limited "overwatch" such as tuning peak demand periods for aircon by forcing a call for the second chiller (by energizing the Y2 relay), but this would sit on top of the primary system, which would still work properly even if the Pi was dead or disconnected.

## Components
The package consists of the following components:

* HVAC - a Python package used to read and write the status of the HVAC system using GPIO pins on the RPi, consisting of the following modules:
	* hvac - initially, just the status() function that returns a JSON status of the HVAC devices (relays, temp sensors, power); overall interaction with the package
	* Relay - functions associated with accessing the relays on the system, using GPIO pins (one per relay). I have Magnecraft 782/792 (same, 792 is the newer) 2P4T relays. The relays have 24VAC coils, that are energized from various parts of my system, mostly equipment signals from a Honeywell HZ-432 zone control board. The relays are used to drive the equipment (rather than directly from the zone board) because there are complexities, such as the call for cool being served from two separate chillers, turned on serially based on demand (as measured by chiller return water temperature). I use one normally open circuit on each relay to drive a connection to ground for a GPIO pin set with a pullup resistor, so the code sets each pin as a pullup, and then then if the value of the pin is low, the relay is energized. I have eight relays I'm checking status on:
		* ZV - one or more zones is calling to open zone valve(s) and energize zone pump(s)
		* DHW - call for domestic hot water
		* BLR - call for heat
		* LCHL - left chiller
		* RCHL - right chiller
		* Y2ON - demand requires both chillers
		* YOFF - force chillers off for winter or low ambient temp
		* Y2FAN - one or more zones is in Y2 mode with high fan

		Since I'm currently only monitoring, I only use the pins in pullup input mode. If I change later to doing some active energizing of the relays, I will do that using output pins. Since the system relays are energized using 24VAC, this means I would need to use open collectors or secondary relays on the outputs, so that the Pi control voltage (3.3v) can be used to drive the relay voltage via the output (24VAC). I would also put the Pi in parallel on the relay coils, again so if it is not operational the system's mechanical components will continue to function normally.
	
	* Therm - functions associated with 1-wire devices attached to the HVAC system (currently just DS18B20 temperature sensors) - uses w1thermsensor library, simpler interface than the code in OneWire, which just parses the device files from the w1gpio and w1therm modules. Gives you an interface to set the precision on the therms. I have three therms, which are used mainly to monitor status of air conditioning. The system is hydronic (hot water for heat, cold water for aircon) so water temperature is key. The therms monitor the incoming water temp for the header that feeds the secondary circuits (zones), the return water temp from the secondaries, and the chiller return water temp, which is key to deciding how many chillers are needed to satisfy demand (in addition to the setpoint aquastat on each chiller.)
	* OneWire (obsolete) - uses the device files from the one-wire GPIO/therm modbus interface to report temps for attached one-wire therms.
	* Power - a module that calls the stats.htm page for the TED5000 (mine is at 192.168.1.124, hardcoded into Relay.py) and re-formats the status into a JSON object. Currently just gets the values for the MTUs, can easily be modified to get any of the real-time values available on the stats page.
* Local (not done yet) - a local website that invokes the HVAC.status() an returns a formatted web page.
* IOT (not done yet) - a local daemon that polls HVAC.status() once a second and sends the output as an MQTT message to AWS IOT. An AWS Lambda saves off the data via SQS.

## Implementation Notes
I'm using w1thermsensor in Therm.py to implement the temp readings. It's easier than the old school reading the device files and it also gives an interface for setting the precision on the therm (transient or persistent)

My mileage with w1thermsensor: changing the precision on the therm had almost no impact on performance. It takes about one second per sensor regardless. Not sure if the overhead (above the read time spec for the sensor) is due to inefficiencies in the drivers or the python library, but it's slow. I originally wanted to do a one-second sampling for my HVAC, which would work for the other components but not for the therms. Will compromise and do a five-second sampling. This is fine for the therms, not ideal for the TED and relays. I may split out the therm updates separately so I can get one-second sample on the other two (the modular code allows this to be done easily.)

I want the Local interface (a web page you get by hitting the webserver on the Pi) to be simple, so it's going to be a Python CGI that formats a decent styled responsive page. Anything else would be ridiculous overkill. Currently I'm not planning on storing the timeseries data locally, so no need for charting (that plan may change...)

Once I get the MQTT feed set up for AWS IOT, I'll store the data in S3/Dynamo/etc. and get a little more nutty with the charting on the timeseries data.
