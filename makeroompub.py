import requests
import sys
import time


AUTH_TOKEN=["","",""]
USER_ID=""
URL_CREATE="https://api.hipchat.com/v1/rooms/create?format=json&owner_user_id="+USER_ID+"&auth_token="
URL_DEL="https://api.hipchat.com/v1/rooms/delete?format=json&auth_token="

def makeroom(token_nr, room_id):
    makepost = requests.post(URL_CREATE+AUTH_TOKEN[token_nr], data ={"name":"test123", "guest_access":1})
    if makepost.status_code != 200:
        print "well, something went bad making this room. Prolly room didnt get deleted."
        print makepost.json()
        print room_id
        delroom(room_id,token_nr)
        remaining_calls = int(makepost.headers['X-RateLimit-Remaining'])
        if remaining_calls <= 5:
            print "Getting new token" 
            if token_nr == len(AUTH_TOKEN)-1:
                token_nr=0
                print "resetting to 0"
            else:
                token_nr = token_nr + 1
                print "using new token nr: %i" % (token_nr)
        return {'token_nr':token_nr}

    remaining_calls = makepost.headers['X-RateLimit-Remaining']
    if remaining_calls < 5:
        if token_nr == len(AUTH_TOKEN)-1:
            token_nr=0
            print "resetting to 0"
        else:
            token_nr = token_nr + 1
            print "using new token nr: %i" % (token_nr)
            
 
    resultset = makepost.json()
    roomname = resultset['room']['guest_access_url'].replace("https://www.hipchat.com/","")
    roomid = resultset['room']['room_id']
    return {"roomname":roomname,"roomid":roomid}

def writedata(roomname, roomid):
    with open("room.txt","a") as roomfile:
        roomfile.write(roomname + "\n")

def delroom(roomid, token_nr):
    delroom = requests.post(URL_DEL+AUTH_TOKEN[token_nr], data ={"room_id":roomid})

    if delroom.status_code != 200:
        print "well, something went bad deleting this room."
        remaining_calls = int(delroom.headers['X-RateLimit-Remaining'])
        if remaining_calls <= 5:
            print "Getting new token"
            if token_nr == len(AUTH_TOKEN)-1:
                token_nr=0
                print "resetting to 0"
            else:
                token_nr = token_nr + 1
                print "using new token nr: %i" % (token_nr)



token_nr=0
room_id=0
for _ in range(500000):
    result = makeroom(token_nr, room_id)
    if 'token_nr' in result:
        token_nr=result['token_nr']
    
    if 'roomname' in result:
        writedata(result['roomname'],result['roomid'])
        delroom(result['roomid'],token_nr)
        room_id=result['roomid']
        print result['roomname']

print "I'm 100% done" 
