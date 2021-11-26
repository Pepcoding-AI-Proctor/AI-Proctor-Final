import subprocess as sp
import re
import time
from geopy.geocoders import Nominatim

def get_location():

    wt = 5 # Wait time -- I purposefully make it wait before the shell command
    accuracy = 3 #Starting desired accuracy is fine and builds at x1.5 per loop

    time.sleep(wt)
    pshellcomm = ['powershell']
    pshellcomm.append('add-type -assemblyname system.device; '\
                      '$loc = new-object system.device.location.geocoordinatewatcher;'\
                      '$loc.start(); '\
                      'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
                      '{start-sleep -milliseconds 100}; '\
                      '$acc = %d; '\
                      'while($loc.position.location.horizontalaccuracy -gt $acc) '\
                      '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
                      '$loc.position.location.latitude; '\
                      '$loc.position.location.longitude; '\
                      '$loc.position.location.horizontalaccuracy; '\
                      '$loc.stop()' %(accuracy))

    p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
    (out, err) = p.communicate()
    out = re.split('\n', out)

    lat = float(out[0])
    long = float(out[1])
    radius = int(out[2])

    locator = Nominatim(user_agent="myGeocoder")
    coordinates = "{}, {}".format(lat,long)
    location = locator.reverse(coordinates)
    loc = location.raw['address']['state_district'] + ','+ location.raw['address']['state']
    return loc 
