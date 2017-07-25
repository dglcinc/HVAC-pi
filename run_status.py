import logging
logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=logging.WARNING)

from HVAC import hvac

print(hvac.status())
