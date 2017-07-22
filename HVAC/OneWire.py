# Import Libraries
import os
import glob
import time
import logging

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

DS1 = "28-0516a36332ff"
DS2 = "28-0516a365d8ff"
DS3 = "28-0316a00f04ff"
DS4 = "28-0516a36816ff"
DS5 = "28-0316a015e7ff"
device_names = {
    DS1 : "HDR_IN",
    DS2 : "HDR_OUT",
    DS3 : "CRW",
    DS4 : "AMB",
    DS5 : DS5
}
DEVICE_TIMEOUT_SECS = 5

# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'

# returns a JSON object containing the current values of all 28* one-wire devices on the bus
def status(is_celcius=0)
    result = {}
    device_folders = glob.glob(base_dir + '28*')
    for i in device_folders
        device_file = device_folder + '/w1_slave'
        temp = read_temp(device_file, is_celcius)
        device_name = String.replace(device_file, base_dir, "");
        logging.debug("OneWire.device_name = " + device_name)
        keyname = device_names[device_name]
        if keyname == "":
            keyname = device_name
        result[keyname] = temp
    logging.debug(result)
    return result

# A function that reads the sensors data
def read_temp_raw(device_file):
  f = open(device_file, 'r') # Opens the temperature device file
  lines = f.readlines() # Returns the text
  f.close()
  return lines

# Convert the value of the sensor into a temperature
def read_temp(device_file, is_celcius=0):
  lines = read_temp_raw(device_file) # Read the temperature 'device file'

  # While the first line does not contain 'YES', wait for 0.2s
  # and then read the device file again.
  timeout_count = DEVICE_TIMEOUT_SECS*5
  while lines[0].strip()[-3:] != 'YES' && timeout_count > 0:
    time.sleep(0.2)
    lines = read_temp_raw()
    timeout_count = timeout_count-1

  # Look for the position of the '=' in the second line of the
  # device file.
  equals_pos = lines[1].find('t=')

  # If the '=' is found, convert the rest of the line after the
  # '=' into degrees Celsius, then degrees Fahrenheit
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c if is_celcius else temp_f
  else
    return -1

