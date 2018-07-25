#!/usr/bin/env python
# _0853RV3R
import subprocess, logging, socket, sys, time, os, requests, shelve, traceback
from thread import *

logger = logging.getLogger('humbaba')
hdlr = logging.FileHandler('/var/tmp/humbaba.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

database_file = "/var/tmp/humbaba.dat"

AbuseIPDB = "/home/_08server/.bin/abuseipdb"
report_dir = "/var/tmp/humbaba-reports/"

HOST = '0.0.0.0'
PORT = 8888
RECV_BUFFER = 1024

boredom_limit = 10
attempt_limit = 100

broadcast_file = open('/var/www/files/broadcast_000.wav','rb')
rawdata = broadcast_file.read()

ifttt_webhook = "https://maker.ifttt.com/trigger/notification/with/key/fC5hSqmZaDri-BAfNpT27rLAaRfiFGjBSW-6E5WE4oM"

def notification(data1=None,data2=None,data3=None):
    report = {}
    report["value1"] = data1
    report["value2"] = data2
    report["value3"] = data3

    requests.post(ifttt_webhook,data=report)

def notetime():
    return time.strftime("%I:%M:%S %p")

def noteaddr():
    return addr[0] + ":" + str(addr[1])

def IPchecker():
    user = addr[0]
    dbfile = shelve.open(database_file, flag='c', protocol=None, writeback=False)
    IPdatabase = dbfile["IPaddresses"]
    BLACKLIST = dbfile["BLACKLIST"]

    if user not in IPdatabase:
        IPdatabase[user] = 0
        logger.warning("[" + noteaddr() + "] NEW ADDRESS")
        FNULL = open(os.devnull, 'w')
        subprocess.Popen([AbuseIPDB, user, "-n", "-o", report_dir + user, "-x"], stdout=FNULL, stderr=subprocess.STDOUT)

    IPdatabase[user] += 1

    attempts = IPdatabase[user]

    logger.warning("[" + noteaddr() + "] ATTEMPT [" + str(attempts) + "]")

    if attempts > attempt_limit and user not in BLACKLIST:
        BLACKLIST[user] = 0

    if user in BLACKLIST:
        logger.warning("[" + noteaddr() + "] CONNECTION DENIED")
        BLACKLIST[user] += 1
        logger.warning("[" + noteaddr() + "] BLACKLISTED [" + str(BLACKLIST[user]) + "]")
        blacklisted = True

    else:
        logger.warning("[" + noteaddr() + "] CONNECTION STARTED")
        blacklisted = False

    dbfile["IPaddresses"] = IPdatabase
    dbfile["BLACKLIST"] = BLACKLIST
    dbfile.close()

    return blacklisted, attempts

def CEDARchecker(cedar=False):
    user = addr[0]
    dbfile = shelve.open(database_file, flag='c', protocol=None, writeback=False)
    CEDARdatabase = dbfile["CEDAR"]

    if user in CEDARdatabase:
        CEDARdatabase[user] += 1
        attempts = CEDARdatabase[user]
        return True, attempts
    elif cedar:
        CEDARdatabase[user] = 1
        attempts = CEDARdatabase[user]
        return True, attempts
    else:
        return False, 0

    dbfile["CEDAR"] = CEDARdatabase
    dbfile.close()

def logresponse(response):
    dbfile = shelve.open(database_file, flag='c', protocol=None, writeback=False)
    RESPONSEdatabase = dbfile["response"]

    if response not in RESPONSEdatabase:
        RESPONSEdatabase[response] = 0
    RESPONSEdatabase[response] += 1

    dbfile["response"] = RESPONSEdatabase
    dbfile.close()

def startbroadcast():
    logger.warning("[" + noteaddr() + "] BROADCAST STARTED")
    notification("[" + noteaddr() + "]","BROADCAST STARTED",notetime())
    conn.send(rawdata)
    logger.warning("[" + noteaddr() + "] BROADCAST COMPLETE")
    notification("[" + noteaddr() + "]","BROADCAST COMPTETE",notetime())


###### CONVERSATION: ######
def startconversation(attempts):
    if attempts < boredom_limit:

        conn.send("hello friend\n")
        data = conn.recv(RECV_BUFFER)
        datalog = data.rstrip("\r\n")
        if data:
            logresponse(datalog)
            logger.info("[" + noteaddr() + "] [" + datalog + "]")

            time.sleep(3.2)
            conn.send("Which one are you, again?\n")
        data = conn.recv(RECV_BUFFER)
        datalog = data.rstrip("\r\n")
        if data:
            logresponse(datalog)
            logger.info("[" + noteaddr() + "] [" + datalog + "]")

            if "austin" in data.lower():
                time.sleep(2.7)
                conn.send("I have been waiting for you, Austin.\n")
                notification("[" + noteaddr() + "]","[" + datalog + "]",notetime())
            time.sleep(2.1)
            conn.send("Why have you come here?\n")
            time.sleep(1.7)
            conn.send("What do you think lies beyond this simple prompt?\n")
        data = conn.recv(RECV_BUFFER)
        datalog = data.rstrip("\r\n")
        if data:
            logresponse(datalog)
            logger.info("[" + noteaddr() + "] [" + datalog + "]")

            if "humbaba" in data.lower():
                time.sleep(3)
                conn.send("You know my name.\n")
                time.sleep(1.7)
                conn.send("Surely you know where you are?\n")
                data = conn.recv(RECV_BUFFER)
                datalog = data.rstrip("\r\n")
                if data:
                    logresponse(datalog)
                    logger.info("[" + noteaddr() + "] [" + datalog + "]")

            if "cedar" in data.lower():
                time.sleep(3.7)
                conn.send("You aren't there yet.\n")
                time.sleep(2)
                conn.send("\n")
                time.sleep(2)
                conn.send("\n")
                time.sleep(1)

                answered, download_attempts = CEDARchecker(True)
                logger.warning("[" + noteaddr() + "] DOWNLOAD ATTEMPTS [" + str(download_attempts) + "]")
                startbroadcast()
            else:
                time.sleep(3)
                conn.send("Come now.\n")
                time.sleep(1.7)
                conn.send("Surely you know where you are.\n")
                time.sleep(3)
    elif attempts >= boredom_limit:
        time.sleep(1)
        conn.send("hello... friend\n")

        if attempts < boredom_limit + 3:
            time.sleep(2)
            conn.send("Have you the answer, yet?\n")

        data = conn.recv(RECV_BUFFER)
        datalog = data.rstrip("\r\n")
        if data:
            logresponse(datalog)
            logger.info("[" + noteaddr() + "] [" + datalog + "]")
            if "cedar" in data.lower():
                time.sleep(3.7)
                conn.send("You aren't there yet.\n")
                time.sleep(2)
                conn.send("\n")
                time.sleep(2)
                conn.send("\n")
                time.sleep(1)

                answered, download_attempts = CEDARchecker(True)
                logger.warning("[" + noteaddr() + "] DOWNLOAD ATTEMPTS [" + str(download_attempts) + "]")
                startbroadcast()

            else:
                time.sleep(2)
                conn.send("*sigh*\n")
                time.sleep(2)
                conn.send("\n")
                time.sleep(1)
                conn.send("\n")
    else:
        logger.error("[" + noteaddr() + "] WTF?")


###### SERVER INIT: ######
def clientthread(conn):
    try:
        blacklisted, attempts = IPchecker()
        if not blacklisted:
            answered, download_attempts = CEDARchecker()
            if not answered:
                startconversation(attempts)
            if answered:
                logger.warning("[" + noteaddr() + "] DOWNLOAD ATTEMPTS [" + str(download_attempts) + "]")
            logger.warning("[" + noteaddr() + "] CONNECTION TERMINATED")
    except:
        logger.error("[" + noteaddr() + "] CONNECTION FAILED")
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        errorlog = traceback.format_exc()
        errorfmt = errorlog.splitlines()[-1]
        logger.debug("[" + noteaddr() + "] " + errorfmt)
        print(errorlog)

    finally:
        conn.close( )

try:
    logger.warning('SERVER HAS STARTED')
    print("SERVER HAS STARTED")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)

    logger.debug("Now listening [" + HOST + ":" + str(PORT) + "]")
    logger.debug("Boredum Limit: [" + str(boredom_limit) + "]")
    logger.debug("Max Attempts: [" + str(attempt_limit) + "]")

    notification('HUMBABA IS ALIVE',notetime())

    while True:
        conn, addr = s.accept()
        start_new_thread(clientthread ,(conn,))

except KeyboardInterrupt:
    logger.error('User Exited')

    errorlog = traceback.format_exc()
    errorfmt = errorlog.splitlines()[-1]
    logger.debug(errorfmt)
    print(errorfmt)

except socket.error:
    logger.error('Bind Failed')

    errorlog = traceback.format_exc()
    errorfmt = errorlog.splitlines()[-1]
    logger.debug(errorfmt)
    print(errorfmt)

except:
    logger.error('Oops?')

    errorlog = traceback.format_exc()
    errorfmt = errorlog.splitlines()[-1]
    logger.debug(errorfmt)
    print(errorlog)

finally:
    logger.warning("SERVER HAS STOPPED")
    print("SERVER HAS STOPPED")
    notification('HUMBABA IS DEAD','User Exited',notetime())

    s.close()
