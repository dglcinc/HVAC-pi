import logging
import sys

logger = logging.getLogger(__name__)
dlevel = logging.WARNING

if len(sys.argv) > 1:
    logger.debug("Setting log level to: " + sys.argv[1])
    dlevel = sys.argv[1]

logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=dlevel)
logger.debug(sys.argv)

from HVAC import Relay

print(Relay.status())
