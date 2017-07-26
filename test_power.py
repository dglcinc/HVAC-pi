import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.WARNING)

import HVAC.Power

print(HVAC.Power.status())

'''
Requires the GPIO setup with one-wire devices attached
'''
