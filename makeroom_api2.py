#lets try it the nice way
import requests, sys, time, threading, logging, json

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

APIToken=["","", "", "", "","","","","",""]
roomNames=["apiv2room-1", "apiv2room-2", "apiv2room-3","apiv2room-4","apiv2room-5","apiv2room-6","apiv2room-7","apiv2room-8","apiv2room-9","apiv2room-10"]

#if a room has guest access enabled, turn it off!
def disableInitialRoomGuestAccess(roomName, APIToken):
    #get room info
    logging.debug('Starting')
    roomURL= "https://api.hipchat.com/v2/room/" + roomName + "?auth_token=" + APIToken
    getInfo = requests.get(roomURL)
    remaining_calls = int(getInfo.headers['X-RateLimit-Remaining'])
    logging.info('Remaining calls for this API Key: %i' % (remaining_calls))

    if getInfo.status_code != 200:
        logging.info('status code: %s' % (getInfo.status_code))
        if getInfo.status_code == 429:
            logger.info("out of keys, sleeping")
            time.sleep(60)
            logger.info("lets try again")
        #lets just try again ;)
        disableInitialRoomGuestAccess(roomName, APIToken)
    isName = getInfo.json()['name']
    isGuestAccessible = getInfo.json()['is_guest_accessible']
    logging.info("room %s is set to is_guest_accessible: %s " % (isName,isGuestAccessible))
    
    #turn off if the room is guest accessible
    if isGuestAccessible:
        logging.info("changing room %s to is_guest_accessible: False" % (isName))
        payload = getInfo.json()
        payload['is_guest_accessible'] = False
        resultPut = requests.put(roomURL, data = json.dumps(payload), headers={'content-type':'application/json'})
        remaining_calls = int(resultPut.headers['X-RateLimit-Remaining'])
        logging.info('Remaining calls for this API Key: %i' % (remaining_calls))

        if resultPut.status_code == 204:
            logging.info("Done!")
        else:
            logging.info(resultPut.status_code)
            logger.info("out of keys, sleeping")
            time.sleep(60)
            logger.info("lets try again")
    return

# thread turn initial guest access off
#only runs at start, to disable any guest access that might be 
#enabled from errors
def t_InitGuestAccessOff(roomName,APIToken):
    disableInitialRoomGuestAccess(roomName,APIToken)
    return

#get the room info
def getBasicRoomInfo(roomName,APIToken):
    #get room info
    logging.debug('Starting')
    roomURL= "https://api.hipchat.com/v2/room/" + roomName + "?auth_token=" + APIToken
    getInfo = requests.get(roomURL)
    remainingCalls = int(getInfo.headers['X-RateLimit-Remaining'])
    logging.info('Remaining calls for this API Key: %i' % (remainingCalls))

    if getInfo.status_code != 200:
        logging.info('status code: %s' % (getInfo.status_code))
        if getInfo.status_code == 429:
            logger.info("out of keys, sleeping")
            time.sleep(60)
            logger.info("lets try again")
            #lets just try again ;)
            getBasicRoomInfo(roomName,APIToken)
    return {'getInfo':getInfo.json(), 'remainingCalls':remainingCalls}

def enableGuestAccessReturnURL(roomName, APIToken, basicRoomInfo):
    logging.info("changing room %s to is_guest_accessible: True" % (roomName))
    roomURL= "https://api.hipchat.com/v2/room/" + roomName + "?auth_token=" + APIToken
    payload = basicRoomInfo
    payload['is_guest_accessible'] = True
    resultPut = requests.put(roomURL, data = json.dumps(payload), headers={'content-type':'application/json'})
    remaining_calls = int(resultPut.headers['X-RateLimit-Remaining'])
    logging.info('Remaining calls for this API Key: %i' % (remaining_calls))
    if resultPut.status_code == 204:
        logging.info("Done!")
    else:
        logging.info(resultPut.status_code)
        if getInfo.status_code == 429:
            logger.info("out of keys, sleeping")
            time.sleep(60)
            logger.info("lets try again")
            #lets just try again ;)
            enableGuestAccessReturnURL(roomName, APIToken, basicRoomInfo)

    #now extract the URL we want to know
    resultSet = getBasicRoomInfo(roomName, APIToken)
    guestURL=resultSet['getInfo']['guest_access_url']
    return guestURL.replace("https://www.hipchat.com/","")

def disableGuestAccess(roomName, APIToken, basicRoomInfo):
    logging.info("changing room %s to is_guest_accessible: False" % (roomName))
    roomURL= "https://api.hipchat.com/v2/room/" + roomName + "?auth_token=" + APIToken
    payload = basicRoomInfo
    payload['is_guest_accessible'] = False
    resultPut = requests.put(roomURL, data = json.dumps(payload), headers={'content-type':'application/json'})
    remaining_calls = int(resultPut.headers['X-RateLimit-Remaining'])
    logging.info('Remaining calls for this API Key: %i' % (remaining_calls))
    if resultPut.status_code == 204:
        logging.info("Done!")
    else:
        logging.info(resultPut.status_code)
        if getInfo.status_code == 429:
            logger.info("out of keys, sleeping")
            time.sleep(60)
            logger.info("lets try again")
            #lets just try again ;)
            disableGuestAccess(roomName, APIToken, basicRoomInfo)
    return

#here we loop through our tokens till they are spend
def t_LoopTokens(roomName, APIToken, cond):
    #first we get basic room info we need to change data in the room
    #we do this so we can turn on/off without having to request this
    #every single time
    resultSet = getBasicRoomInfo(roomName,APIToken)
    basicRoomInfo = resultSet['getInfo']
    APICallsLeft = resultSet['remainingCalls']

    #now that we have the basic info lets turn guest access on
    #we loop until we are out of tokens
    guestURLStorage=[]
    for _ in range(5):
        guestURL = enableGuestAccessReturnURL(roomName, APIToken, basicRoomInfo)
        logging.info("Guest URL: %s" % (guestURL))
        guestURLStorage.append(guestURL)
        disableGuestAccess(roomName, APIToken, basicRoomInfo)

    #now that we are done looping and have the guest URLs..lets store it someplace safe
    #aquire the file lock
    with cond:
        logging.info("++ writing result to file ++")
        with open("room_api2.txt","a") as roomfile:
            for URLs in guestURLStorage:
                roomfile.write(URLs + "\n")
        #free willie..or the file lock, whatever you prefer
    return

#initial start, no matter the quit, lets start off by disabling
#all the guest access for all rooms
threads = []
for i in range(len(roomNames)):
    t = threading.Thread(target=t_InitGuestAccessOff, args=(roomNames[i],APIToken[i]))
    threads.append(t)
    t.start()
    #lets wait for every thread to be done with that before we continue
t.join()

#now that none of the rooms have guest access enabled, lets loop
#note: we use condition for resource lock on the output file
condition = threading.Condition()
keepLooping = True
while keepLooping:
    for i in range(len(roomNames)):
        t = threading.Thread(target=t_LoopTokens, args=(roomNames[i], APIToken[i], condition,))
        threads.append(t)
        t.start()
    t.join()
