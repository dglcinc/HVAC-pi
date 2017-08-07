from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import sys
import os

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.WARNING)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# open the connection
myClient = AWSIoTMQTTClient("HVAC-pi",useWebsocket=True)
myClient.configureEndpoint("afqodfj0vu81r.iot.us-east-1.amazonaws.com",443)
myClient.configureCredentials("/home/pi/github/HVAC-pi/local/root_ca.txt")

# configure it
myClient.configureOfflinePublishQueueing(-1)
myClient.configureDrainingFrequency(2)
myClient.configureConnectDisconnectTimeout(10)
myClient.configureMQTTOperationTimeout(5)

def updateRPiThing(jsonstr):
    logger.debug("updating Rpi thing...")
    myClient.connect()
    myClient.publish("$aws/things/68Lookout-HVAC/shadow/update", jsonstr, 0)
    return
