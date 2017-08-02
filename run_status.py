import logging
import sys
import os
import time

logger = logging.getLogger(__name__)
logger.debug(sys.argv)
dlevel = logging.WARNING

CYCLE_SECS = 10

OM_DAEMON = 1
OM_EXIT = 2
OM_RUN = 3

opmode = OM_RUN

if len(sys.argv) > 1:
    args = sys.argv[1:]
    logger.debug("Args = " + str(args))
    for arg in args:
        if arg == "DEBUG" or arg == "INFO" or arg == "WARNING":
            logger.debug("Setting log level to: " + sys.argv[1])
            dlevel = arg
        elif arg == "DAEMON":
            opmode = OM_DAEMON
        else:
            logger.exception("Unknown argument: " + arg)
            opmode = OM_EXIT

logger.debug("Arg loading done.")

def get_lock(lock_file="/tmp/hvac_pi.pid"):
    try:
        logger.debug("Checking for lock.")
        if os.access(lock_file, os.F_OK):
            #if the lockfile is already there then check the PID number
            #in the lock file
            pidfile = open(lock_file, "r")
            pidfile.seek(0)
            old_pid = pidfile.readline()
    
            # Now we check the PID from lock file matches to the current
            # process PID
            if os.path.exists("/proc/%s" % old_pid):
                logger.debug("It is running as process %s," % old_pid)
                sys.exit(1)
            else:
                logger.debug("File is there but the program is not running")
                logger.debug("Removing lock file for the: %s as it can be there because of the program last time it was run" % old_pid)
                os.remove(lock_file)
        pidfile = open(lock_file, "w")
        pidfile.write("%s" % os.getpid())
        pidfile.close()
    except IOError:
        logger.exception("Unable to handle pid file cleanly.")
        sys.exit(1)
    return
    
from HVAC import hvac

if opmode == OM_RUN:
    logging.basicConfig(format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=dlevel)
    print(hvac.status())
if opmode == OM_DAEMON:
    logging.basicConfig(filename="/var/log/hvac/hvac.log",format='%(name)s %(levelname)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S',level=dlevel)
    get_lock()

    while True:
        timestamp = time.time()
        logger.debug("New run, timestamp = " + str(timestamp))
        data = hvac.status()
        f = open("/tmp/hvac_current.json","w")
        if f:
            logger.debug("Data = " + str(data))
            f.write(data)
            f.close()
        else:
            logger.warning("Unable to open data file")
        # start a run as close to every X seconds as possible
        while (time.time() - timestamp) < CYCLE_SECS:
            time.sleep(0.5)
