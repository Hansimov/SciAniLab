from datetime import *
from time import *
from math import *
import requests
import json




invars_file = open('invars.json','r+')
# invars_str = invars_file.read()
# invars = json.loads(invars_str)
invars = json.load(invars_file)
invars_file.close()


def updateInvarsFile():
    global invars
    invars_file = open('invars.json','w+')
    # invars_str = json.dumps(invars)
    # invars_file.write(invars_str)
    json.dump(invars, invars_file)
    invars_file.close()



